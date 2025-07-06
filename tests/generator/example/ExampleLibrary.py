"""
Example Library for demonstrating test generation strategies.
Contains only print statements to show the workflow without complex implementation.
"""

class ExampleLibrary:
    """Robot Framework library for the simple example machine."""
    
    def __init__(self):
        self.user = None
        self.action = None
    
    def setup_example_environment(self):
        """Setup the example environment."""
        print("🚀 Setting up example environment")
        print("   Environment is ready for testing")
    
    def authenticate_user(self):
        """Authenticate the current user."""
        print(f"🔐 Authenticating user: {self.user}")
        if hasattr(self, '_machine_variables'):
            user_var = self._machine_variables.get('USER', 'unknown')
            print(f"   User variable: {user_var}")
        print("   Authentication process completed")
    
    def perform_action(self):
        """Perform the current action."""
        print(f"⚡ Performing action: {self.action}")
        if hasattr(self, '_machine_variables'):
            action_var = self._machine_variables.get('ACTION', 'unknown')
            print(f"   Action variable: {action_var}")
        print("   Action execution completed")
    
    def logout(self):
        """Log out the current user."""
        print("👋 User logging out")
        print("   Session terminated successfully")
    
    def retry_authentication(self):
        """Retry the authentication process."""
        print("🔄 Retrying authentication")
        print("   Preparing for new authentication attempt")
    
    def exit_system(self):
        """Exit the system."""
        print("🚪 Exiting system")
        print("   System shutdown initiated")
    
    def continue_working(self):
        """Continue working after successful action."""
        print("✅ Continuing work")
        print("   Ready for next operation")
    
    def retry_action(self):
        """Retry the failed action."""
        print("🔁 Retrying action")
        print("   Preparing for action retry")
    
    def restart_system(self):
        """Restart the system."""
        print("🔄 Restarting system")
        print("   System restart initiated")
    
    def set_machine_variables(self, user, action):
        """Set the machine variables for this test run."""
        self.user = user
        self.action = action
        if not hasattr(self, '_machine_variables'):
            self._machine_variables = {}
        self._machine_variables['USER'] = user
        self._machine_variables['ACTION'] = action
        print("📝 Set machine variables:")
        print(f"   USER = {user}")
        print(f"   ACTION = {action}")


# Robot Framework keywords (functions that can be called directly)
def setup_example_environment():
    """Setup keyword for Robot Framework."""
    lib = ExampleLibrary()
    lib.setup_example_environment()

def authenticate_user():
    """Authenticate user keyword."""
    print("🔐 Authenticating user")
    print("   Authentication logic executed")

def perform_action():
    """Perform action keyword."""
    print("⚡ Performing action")
    print("   Action logic executed")

def logout():
    """Logout keyword."""
    print("👋 Logging out")
    print("   Logout logic executed")

def retry_authentication():
    """Retry authentication keyword."""
    print("🔄 Retrying authentication")
    print("   Retry authentication logic executed")

def exit_system():
    """Exit system keyword."""
    print("🚪 Exiting system")
    print("   Exit system logic executed")

def continue_working():
    """Continue working keyword."""
    print("✅ Continuing working")
    print("   Continue working logic executed")

def retry_action():
    """Retry action keyword."""
    print("🔁 Retrying action")
    print("   Retry action logic executed")

def restart_system():
    """Restart system keyword."""
    print("🔄 Restarting system")
    print("   Restart system logic executed")

def print_test_separator(test_name):
    """Print a separator for test organization."""
    print("=" * 60)
    print(f"  {test_name}")
    print("=" * 60)
