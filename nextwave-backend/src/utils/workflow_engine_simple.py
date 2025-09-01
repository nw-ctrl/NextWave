class WorkflowEngine:
    def __init__(self):
        self.workflows = {}
    
    def create_workflow(self, name, description=""):
        workflow = {
            'id': f'workflow_{len(self.workflows) + 1}',
            'name': name,
            'description': description
        }
        self.workflows[workflow['id']] = workflow
        return type('Workflow', (), workflow)()
    
    def list_workflows(self):
        return list(self.workflows.values())
    
    def execute_workflow(self, workflow_id, input_data=None):
        return {
            'execution_id': f'exec_{workflow_id}',
            'status': 'completed',
            'result': 'success'
        }
    
    def create_sample_workflows(self):
        # Create some sample workflows
        self.create_workflow("Document Processing", "Process PDF documents")
        self.create_workflow("Image Analysis", "Analyze uploaded images")

