import json
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
import asyncio
import threading
from queue import Queue

class StepType(Enum):
    INPUT = "input"
    PROCESSING = "processing"
    VALIDATION = "validation"
    OUTPUT = "output"
    CONDITION = "condition"
    LOOP = "loop"
    API_CALL = "api_call"
    TRANSFORM = "transform"

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class WorkflowStep:
    def __init__(self, step_id: str, name: str, step_type: StepType, config: Dict[str, Any] = None):
        self.id = step_id
        self.name = name
        self.type = step_type
        self.config = config or {}
        self.status = StepStatus.PENDING
        self.input_data = None
        self.output_data = None
        self.error_message = None
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.next_steps = []
        self.previous_steps = []
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'status': self.status.value,
            'config': self.config,
            'input_data': self.input_data,
            'output_data': self.output_data,
            'error_message': self.error_message,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'next_steps': self.next_steps,
            'previous_steps': self.previous_steps
        }

class WorkflowExecution:
    def __init__(self, workflow_id: str, execution_id: str = None):
        self.workflow_id = workflow_id
        self.execution_id = execution_id or str(uuid.uuid4())
        self.status = StepStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.steps_executed = []
        self.current_step = None
        self.error_message = None
        self.input_data = {}
        self.output_data = {}
        self.execution_log = []
    
    def log(self, message: str, level: str = "info"):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'step_id': self.current_step.id if self.current_step else None
        }
        self.execution_log.append(log_entry)
    
    def to_dict(self):
        return {
            'workflow_id': self.workflow_id,
            'execution_id': self.execution_id,
            'status': self.status.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'steps_executed': [step.to_dict() for step in self.steps_executed],
            'current_step': self.current_step.to_dict() if self.current_step else None,
            'error_message': self.error_message,
            'input_data': self.input_data,
            'output_data': self.output_data,
            'execution_log': self.execution_log
        }

class Workflow:
    def __init__(self, workflow_id: str, name: str, description: str = ""):
        self.id = workflow_id
        self.name = name
        self.description = description
        self.steps = {}
        self.start_step_id = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.version = "1.0.0"
        self.is_active = True
        self.execution_count = 0
    
    def add_step(self, step: WorkflowStep):
        self.steps[step.id] = step
        self.updated_at = datetime.now()
    
    def connect_steps(self, from_step_id: str, to_step_id: str):
        if from_step_id in self.steps and to_step_id in self.steps:
            self.steps[from_step_id].next_steps.append(to_step_id)
            self.steps[to_step_id].previous_steps.append(from_step_id)
            self.updated_at = datetime.now()
    
    def set_start_step(self, step_id: str):
        if step_id in self.steps:
            self.start_step_id = step_id
            self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'steps': {step_id: step.to_dict() for step_id, step in self.steps.items()},
            'start_step_id': self.start_step_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version': self.version,
            'is_active': self.is_active,
            'execution_count': self.execution_count
        }

class WorkflowEngine:
    def __init__(self):
        self.workflows = {}
        self.executions = {}
        self.step_processors = {
            StepType.INPUT: self._process_input_step,
            StepType.PROCESSING: self._process_processing_step,
            StepType.VALIDATION: self._process_validation_step,
            StepType.OUTPUT: self._process_output_step,
            StepType.CONDITION: self._process_condition_step,
            StepType.TRANSFORM: self._process_transform_step,
            StepType.API_CALL: self._process_api_call_step
        }
        self.execution_queue = Queue()
        self.is_running = False
    
    def create_workflow(self, name: str, description: str = "") -> Workflow:
        workflow_id = str(uuid.uuid4())
        workflow = Workflow(workflow_id, name, description)
        self.workflows[workflow_id] = workflow
        return workflow
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        return self.workflows.get(workflow_id)
    
    def delete_workflow(self, workflow_id: str) -> bool:
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]
            return True
        return False
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        return [workflow.to_dict() for workflow in self.workflows.values()]
    
    def execute_workflow(self, workflow_id: str, input_data: Dict[str, Any] = None) -> WorkflowExecution:
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if not workflow.start_step_id:
            raise ValueError(f"Workflow {workflow_id} has no start step defined")
        
        execution = WorkflowExecution(workflow_id)
        execution.input_data = input_data or {}
        self.executions[execution.execution_id] = execution
        
        # Start execution in a separate thread
        execution_thread = threading.Thread(
            target=self._execute_workflow_sync,
            args=(workflow, execution)
        )
        execution_thread.start()
        
        workflow.execution_count += 1
        return execution
    
    def _execute_workflow_sync(self, workflow: Workflow, execution: WorkflowExecution):
        try:
            execution.status = StepStatus.RUNNING
            execution.start_time = datetime.now()
            execution.log(f"Starting workflow execution: {workflow.name}")
            
            current_step_id = workflow.start_step_id
            context_data = execution.input_data.copy()
            
            while current_step_id:
                step = workflow.steps.get(current_step_id)
                if not step:
                    execution.log(f"Step {current_step_id} not found", "error")
                    break
                
                execution.current_step = step
                execution.log(f"Executing step: {step.name}")
                
                # Process the step
                success, output_data, next_step_id = self._execute_step(step, context_data, execution)
                
                if success:
                    step.status = StepStatus.COMPLETED
                    step.output_data = output_data
                    context_data.update(output_data or {})
                    execution.steps_executed.append(step)
                    execution.log(f"Step {step.name} completed successfully")
                    
                    # Determine next step
                    if next_step_id:
                        current_step_id = next_step_id
                    elif step.next_steps:
                        current_step_id = step.next_steps[0]  # Take first next step
                    else:
                        current_step_id = None  # End of workflow
                else:
                    step.status = StepStatus.FAILED
                    execution.log(f"Step {step.name} failed: {step.error_message}", "error")
                    execution.status = StepStatus.FAILED
                    execution.error_message = step.error_message
                    break
                
                # Add delay for animation effect
                time.sleep(0.5)
            
            if execution.status != StepStatus.FAILED:
                execution.status = StepStatus.COMPLETED
                execution.output_data = context_data
                execution.log("Workflow execution completed successfully")
            
            execution.end_time = datetime.now()
            execution.duration = (execution.end_time - execution.start_time).total_seconds()
            execution.current_step = None
            
        except Exception as e:
            execution.status = StepStatus.FAILED
            execution.error_message = str(e)
            execution.log(f"Workflow execution failed: {str(e)}", "error")
            execution.end_time = datetime.now()
            if execution.start_time:
                execution.duration = (execution.end_time - execution.start_time).total_seconds()
    
    def _execute_step(self, step: WorkflowStep, context_data: Dict[str, Any], execution: WorkflowExecution):
        try:
            step.status = StepStatus.RUNNING
            step.start_time = datetime.now()
            step.input_data = context_data.copy()
            
            # Get the appropriate processor for this step type
            processor = self.step_processors.get(step.type)
            if not processor:
                raise ValueError(f"No processor found for step type: {step.type}")
            
            # Execute the step
            success, output_data, next_step_id = processor(step, context_data, execution)
            
            step.end_time = datetime.now()
            step.duration = (step.end_time - step.start_time).total_seconds()
            
            return success, output_data, next_step_id
            
        except Exception as e:
            step.status = StepStatus.FAILED
            step.error_message = str(e)
            step.end_time = datetime.now()
            if step.start_time:
                step.duration = (step.end_time - step.start_time).total_seconds()
            return False, None, None
    
    def _process_input_step(self, step: WorkflowStep, context_data: Dict[str, Any], execution: WorkflowExecution):
        # Simulate input processing
        time.sleep(1)
        
        input_config = step.config.get('input', {})
        required_fields = input_config.get('required_fields', [])
        
        # Validate required fields
        for field in required_fields:
            if field not in context_data:
                step.error_message = f"Required field '{field}' not found in input"
                return False, None, None
        
        # Process input data
        output_data = {
            'processed_input': True,
            'input_fields': list(context_data.keys()),
            'timestamp': datetime.now().isoformat()
        }
        
        return True, output_data, None
    
    def _process_processing_step(self, step: WorkflowStep, context_data: Dict[str, Any], execution: WorkflowExecution):
        # Simulate processing
        processing_time = step.config.get('processing_time', 2)
        time.sleep(processing_time)
        
        operation = step.config.get('operation', 'default')
        
        if operation == 'document_processing':
            output_data = {
                'processed_document': True,
                'document_type': context_data.get('document_type', 'unknown'),
                'pages_processed': context_data.get('page_count', 1),
                'processing_result': 'success'
            }
        elif operation == 'image_analysis':
            output_data = {
                'analyzed_image': True,
                'image_format': context_data.get('image_format', 'unknown'),
                'analysis_result': {
                    'brightness': 142,
                    'dominant_color': '#3b82f6',
                    'objects_detected': 3
                }
            }
        else:
            output_data = {
                'processed': True,
                'operation': operation,
                'result': 'completed'
            }
        
        return True, output_data, None
    
    def _process_validation_step(self, step: WorkflowStep, context_data: Dict[str, Any], execution: WorkflowExecution):
        # Simulate validation
        time.sleep(0.5)
        
        validation_rules = step.config.get('rules', [])
        validation_results = []
        
        for rule in validation_rules:
            field = rule.get('field')
            condition = rule.get('condition')
            value = rule.get('value')
            
            if field in context_data:
                field_value = context_data[field]
                
                if condition == 'equals' and field_value == value:
                    validation_results.append({'rule': rule, 'passed': True})
                elif condition == 'not_empty' and field_value:
                    validation_results.append({'rule': rule, 'passed': True})
                else:
                    validation_results.append({'rule': rule, 'passed': False})
            else:
                validation_results.append({'rule': rule, 'passed': False, 'error': 'Field not found'})
        
        all_passed = all(result['passed'] for result in validation_results)
        
        if not all_passed and step.config.get('fail_on_validation_error', True):
            step.error_message = "Validation failed"
            return False, None, None
        
        output_data = {
            'validation_passed': all_passed,
            'validation_results': validation_results
        }
        
        return True, output_data, None
    
    def _process_output_step(self, step: WorkflowStep, context_data: Dict[str, Any], execution: WorkflowExecution):
        # Simulate output generation
        time.sleep(1)
        
        output_format = step.config.get('format', 'json')
        output_fields = step.config.get('fields', list(context_data.keys()))
        
        output_data = {
            'output_generated': True,
            'format': output_format,
            'output_data': {field: context_data.get(field) for field in output_fields if field in context_data}
        }
        
        return True, output_data, None
    
    def _process_condition_step(self, step: WorkflowStep, context_data: Dict[str, Any], execution: WorkflowExecution):
        # Simulate condition evaluation
        time.sleep(0.2)
        
        condition = step.config.get('condition', {})
        field = condition.get('field')
        operator = condition.get('operator', 'equals')
        value = condition.get('value')
        
        if field not in context_data:
            step.error_message = f"Condition field '{field}' not found"
            return False, None, None
        
        field_value = context_data[field]
        condition_result = False
        
        if operator == 'equals':
            condition_result = field_value == value
        elif operator == 'not_equals':
            condition_result = field_value != value
        elif operator == 'greater_than':
            condition_result = field_value > value
        elif operator == 'less_than':
            condition_result = field_value < value
        
        # Determine next step based on condition
        next_step_id = None
        if condition_result:
            next_step_id = step.config.get('true_step')
        else:
            next_step_id = step.config.get('false_step')
        
        output_data = {
            'condition_result': condition_result,
            'field_value': field_value,
            'expected_value': value
        }
        
        return True, output_data, next_step_id
    
    def _process_transform_step(self, step: WorkflowStep, context_data: Dict[str, Any], execution: WorkflowExecution):
        # Simulate data transformation
        time.sleep(0.5)
        
        transformations = step.config.get('transformations', [])
        transformed_data = context_data.copy()
        
        for transform in transformations:
            operation = transform.get('operation')
            source_field = transform.get('source_field')
            target_field = transform.get('target_field')
            
            if source_field in transformed_data:
                source_value = transformed_data[source_field]
                
                if operation == 'uppercase':
                    transformed_data[target_field] = str(source_value).upper()
                elif operation == 'lowercase':
                    transformed_data[target_field] = str(source_value).lower()
                elif operation == 'multiply':
                    factor = transform.get('factor', 1)
                    transformed_data[target_field] = source_value * factor
                elif operation == 'format_date':
                    # Simplified date formatting
                    transformed_data[target_field] = datetime.now().strftime('%Y-%m-%d')
        
        output_data = {
            'transformed': True,
            'transformations_applied': len(transformations)
        }
        output_data.update(transformed_data)
        
        return True, output_data, None
    
    def _process_api_call_step(self, step: WorkflowStep, context_data: Dict[str, Any], execution: WorkflowExecution):
        # Simulate API call
        time.sleep(1.5)
        
        api_config = step.config.get('api', {})
        url = api_config.get('url')
        method = api_config.get('method', 'GET')
        
        # Simulate API response
        output_data = {
            'api_call_completed': True,
            'url': url,
            'method': method,
            'status_code': 200,
            'response_data': {
                'success': True,
                'message': 'API call simulated successfully'
            }
        }
        
        return True, output_data, None
    
    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        return self.executions.get(execution_id)
    
    def list_executions(self, workflow_id: str = None) -> List[Dict[str, Any]]:
        executions = list(self.executions.values())
        if workflow_id:
            executions = [ex for ex in executions if ex.workflow_id == workflow_id]
        return [execution.to_dict() for execution in executions]
    
    def create_sample_workflows(self):
        """Create sample workflows for demonstration"""
        
        # Document Processing Workflow
        doc_workflow = self.create_workflow(
            "Document Processing Pipeline",
            "Automated document upload, validation, and processing workflow"
        )
        
        # Add steps
        upload_step = WorkflowStep("upload", "Upload Document", StepType.INPUT, {
            'input': {'required_fields': ['document_file', 'document_type']}
        })
        
        validate_step = WorkflowStep("validate", "Validate Format", StepType.VALIDATION, {
            'rules': [
                {'field': 'document_type', 'condition': 'equals', 'value': 'pdf'},
                {'field': 'document_file', 'condition': 'not_empty'}
            ]
        })
        
        process_step = WorkflowStep("process", "Process Document", StepType.PROCESSING, {
            'operation': 'document_processing',
            'processing_time': 3
        })
        
        output_step = WorkflowStep("output", "Generate Output", StepType.OUTPUT, {
            'format': 'json',
            'fields': ['processed_document', 'document_type', 'pages_processed']
        })
        
        # Add steps to workflow
        doc_workflow.add_step(upload_step)
        doc_workflow.add_step(validate_step)
        doc_workflow.add_step(process_step)
        doc_workflow.add_step(output_step)
        
        # Connect steps
        doc_workflow.connect_steps("upload", "validate")
        doc_workflow.connect_steps("validate", "process")
        doc_workflow.connect_steps("process", "output")
        doc_workflow.set_start_step("upload")
        
        # Image Analysis Workflow
        img_workflow = self.create_workflow(
            "Image Analysis Pipeline",
            "AI-powered image analysis and report generation workflow"
        )
        
        img_upload_step = WorkflowStep("img_upload", "Upload Image", StepType.INPUT, {
            'input': {'required_fields': ['image_file', 'image_format']}
        })
        
        img_process_step = WorkflowStep("img_analyze", "Analyze Image", StepType.PROCESSING, {
            'operation': 'image_analysis',
            'processing_time': 2
        })
        
        img_output_step = WorkflowStep("img_output", "Generate Report", StepType.OUTPUT, {
            'format': 'pdf',
            'fields': ['analyzed_image', 'analysis_result']
        })
        
        img_workflow.add_step(img_upload_step)
        img_workflow.add_step(img_process_step)
        img_workflow.add_step(img_output_step)
        
        img_workflow.connect_steps("img_upload", "img_analyze")
        img_workflow.connect_steps("img_analyze", "img_output")
        img_workflow.set_start_step("img_upload")

