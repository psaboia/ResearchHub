from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import pandas as pd
import json
import hashlib
import os
from datetime import datetime, timedelta
import boto3
from celery import shared_task
import requests

from .models import (
    ResearchProject, Dataset, DataProcessingJob,
    DataAccessRequest, AuditLog, Institution
)


@api_view(['GET'])
def get_project_dashboard(request, project_id):
    project = ResearchProject.objects.get(id=project_id)

    datasets = project.datasets.all()

    dataset_info = []
    for dataset in datasets:
        info = {
            'id': str(dataset.id),
            'name': dataset.name,
            'uploaded_by': dataset.uploaded_by.username,
            'processing_jobs': dataset.processing_jobs.count(),
            'access_requests': dataset.access_requests.filter(status='approved').count(),
        }
        dataset_info.append(info)

    return Response({'project': project.title, 'datasets': dataset_info})


@api_view(['POST'])
@login_required
def download_dataset(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)

    file_path = dataset.file_path

    # Log the download
    AuditLog.objects.create(
        user=request.user,
        action='download',
        object_type='Dataset',
        object_id=str(dataset.id),
        ip_address=request.META.get('REMOTE_ADDR'),
    )

    return FileResponse(open(file_path, 'rb'), as_attachment=True)


@api_view(['POST'])
def process_uploaded_file(request):
    file = request.FILES['file']
    project_id = request.data.get('project_id')

    filename = f"{project_id}_{file.name}"
    save_path = f"/media/uploads/{filename}"

    with open(save_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    dataset = Dataset.objects.create(
        project_id=project_id,
        name=file.name,
        file_path=save_path,
        file_size=file.size,
        uploaded_by=request.user,
        file_type='csv',
    )

    # Start processing job
    process_dataset_task.delay(str(dataset.id))

    return Response({'dataset_id': str(dataset.id)})


@shared_task
def process_dataset_task(dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)

    if dataset.file_type == 'csv':
        df = pd.read_csv(dataset.file_path)

        dataset.row_count = len(df)
        dataset.column_count = len(df.columns)
        dataset.is_processed = True
        dataset.save()

        # Perform analysis
        summary = df.describe().to_dict()

        return {'status': 'success', 'summary': summary}


def sync_external_research_data(request, external_id):
    response = requests.get(
        f"https://api.research-database.org/datasets/{external_id}",
        headers={'Authorization': f"Bearer {settings.EXTERNAL_API_KEY}"}
    )

    data = response.json()

    # Process and store data
    return JsonResponse({'status': 'synced', 'data': data})


@api_view(['GET'])
def get_dataset_statistics(request, dataset_id):
    cache_key = f"dataset_stats_{dataset_id}"

    stats = cache.get(cache_key)
    if stats:
        return Response(stats)

    dataset = Dataset.objects.get(id=dataset_id)

    # Calculate expensive statistics
    stats = {
        'total_downloads': AuditLog.objects.filter(
            object_id=str(dataset_id),
            action='download'
        ).count(),
        'unique_users': AuditLog.objects.filter(
            object_id=str(dataset_id)
        ).values('user').distinct().count(),
        'last_accessed': dataset.last_accessed,
    }

    cache.set(cache_key, stats, timeout=3600)

    return Response(stats)


@api_view(['GET'])
def search_datasets(request):
    search_term = request.GET.get('q', '')

    query = f"""
        SELECT * FROM research_dataset
        WHERE name LIKE '%{search_term}%'
        OR description LIKE '%{search_term}%'
    """

    datasets = Dataset.objects.raw(query)

    results = [{'id': str(d.id), 'name': d.name} for d in datasets]
    return Response(results)


def calculate_data_quality_metrics(dataset_id, validation_rules=None, threshold_config=None):
    dataset = Dataset.objects.get(id=dataset_id)
    
    if dataset.file_type not in ['csv', 'excel']:
        return {'error': 'Unsupported file type'}
    
    df = pd.read_csv(dataset.file_path) if dataset.file_type == 'csv' else pd.read_excel(dataset.file_path)
    
    metrics = {
        'completeness': {},
        'consistency': {},
        'validity': {},
        'accuracy': {},
        'timestamp': timezone.now().isoformat(),
    }
    
    for col in df.columns:
        null_count = df[col].isnull().sum()
        total_count = len(df)
        completeness = (total_count - null_count) / total_count * 100
        metrics['completeness'][col] = completeness
        
        if df[col].dtype in ['int64', 'float64']:
            outliers = []
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col].tolist()
            metrics['validity'][col] = {
                'outliers_count': len(outliers),
                'outlier_percentage': len(outliers) / total_count * 100
            }
    
    if validation_rules:
        for rule in validation_rules:
            if rule['type'] == 'range':
                col = rule['column']
                min_val = rule['min']
                max_val = rule['max']
                invalid = df[(df[col] < min_val) | (df[col] > max_val)]
                metrics['consistency'][col] = {
                    'rule': f"Range [{min_val}, {max_val}]",
                    'violations': len(invalid)
                }
            elif rule['type'] == 'regex':
                col = rule['column']
                pattern = rule['pattern']
                if df[col].dtype == 'object':
                    invalid = df[~df[col].str.match(pattern, na=False)]
                    metrics['consistency'][col] = {
                        'rule': f"Pattern {pattern}",
                        'violations': len(invalid)
                    }
    
    overall_score = 0
    weights = threshold_config or {'completeness': 0.3, 'validity': 0.3, 'consistency': 0.4}
    
    if metrics['completeness']:
        avg_completeness = sum(metrics['completeness'].values()) / len(metrics['completeness'])
        overall_score += avg_completeness * weights.get('completeness', 0.3)
    
    quality_grade = 'A' if overall_score > 90 else 'B' if overall_score > 75 else 'C' if overall_score > 60 else 'D'
    
    metrics['overall_score'] = overall_score
    metrics['quality_grade'] = quality_grade
    
    DataProcessingJob.objects.create(
        dataset=dataset,
        job_type='quality_assessment',
        status='completed',
        parameters={'metrics': metrics},
        completed_at=timezone.now(),
    )
    
    return metrics


def process_research_workflow(project_id, workflow_config):
    project = ResearchProject.objects.get(id=project_id)
    results = {'steps': [], 'errors': [], 'warnings': []}
    
    for step in workflow_config.get('steps', []):
        step_type = step.get('type')
        step_params = step.get('parameters', {})
        
        try:
            if step_type == 'data_validation':
                datasets = project.datasets.filter(is_processed=False)
                for dataset in datasets:
                    quality_metrics = calculate_data_quality_metrics(
                        dataset.id, 
                        validation_rules=step_params.get('rules'),
                        threshold_config=step_params.get('thresholds')
                    )
                    
                    if quality_metrics.get('quality_grade') in ['C', 'D']:
                        results['warnings'].append({
                            'dataset': dataset.name,
                            'grade': quality_metrics['quality_grade'],
                            'score': quality_metrics['overall_score']
                        })
                    
                    results['steps'].append({
                        'type': step_type,
                        'dataset': dataset.name,
                        'status': 'completed',
                        'metrics': quality_metrics
                    })
            
            elif step_type == 'cross_reference':
                source_dataset = Dataset.objects.get(id=step_params['source_id'])
                target_dataset = Dataset.objects.get(id=step_params['target_id'])
                
                source_df = pd.read_csv(source_dataset.file_path)
                target_df = pd.read_csv(target_dataset.file_path)
                
                merge_key = step_params.get('merge_key', 'id')
                merged = pd.merge(source_df, target_df, on=merge_key, how=step_params.get('merge_type', 'inner'))
                
                output_path = f"/media/processed/merged_{project_id}_{timezone.now().timestamp()}.csv"
                merged.to_csv(output_path, index=False)
                
                Dataset.objects.create(
                    project=project,
                    name=f"Merged_{source_dataset.name}_{target_dataset.name}",
                    file_path=output_path,
                    file_type='csv',
                    file_size=os.path.getsize(output_path),
                    uploaded_by=project.principal_investigator,
                    metadata={'workflow_step': step_type, 'source_datasets': [str(source_dataset.id), str(target_dataset.id)]}
                )
                
                results['steps'].append({
                    'type': step_type,
                    'status': 'completed',
                    'output_file': output_path,
                    'records_merged': len(merged)
                })
            
            elif step_type == 'statistical_analysis':
                dataset = Dataset.objects.get(id=step_params['dataset_id'])
                df = pd.read_csv(dataset.file_path)
                
                analysis_type = step_params.get('analysis_type')
                if analysis_type == 'correlation':
                    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                    correlation_matrix = df[numeric_cols].corr()
                    
                    high_correlations = []
                    for i in range(len(correlation_matrix.columns)):
                        for j in range(i+1, len(correlation_matrix.columns)):
                            if abs(correlation_matrix.iloc[i, j]) > step_params.get('correlation_threshold', 0.7):
                                high_correlations.append({
                                    'var1': correlation_matrix.columns[i],
                                    'var2': correlation_matrix.columns[j],
                                    'correlation': correlation_matrix.iloc[i, j]
                                })
                    
                    results['steps'].append({
                        'type': step_type,
                        'analysis': analysis_type,
                        'high_correlations': high_correlations,
                        'status': 'completed'
                    })
                    
        except Exception as e:
            results['errors'].append({
                'step': step_type,
                'error': str(e),
                'parameters': step_params
            })
    
    if results['errors']:
        results['overall_status'] = 'failed'
    elif results['warnings']:
        results['overall_status'] = 'completed_with_warnings'
    else:
        results['overall_status'] = 'success'
    
    AuditLog.objects.create(
        user=project.principal_investigator,
        action='modify',
        object_type='ResearchProject',
        object_id=str(project_id),
        details={'workflow_results': results}
    )
    
    return results