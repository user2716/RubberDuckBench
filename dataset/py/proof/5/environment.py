import os

def _eval_value(value_string):
  """Returns evaluated value."""
  try:
    return ast.literal_eval(value_string)
  except:
    # String fallback.
    return value_string

def get_value(environment_variable, default_value=None):
  """Return an environment variable value."""
  value_string = os.getenv(environment_variable)

  # value_string will be None if the variable is not defined.
  if value_string is None:
    return default_value

  # Exception for ANDROID_SERIAL. Sometimes serial can be just numbers,
  # so we don't want to it eval it.
  if environment_variable == 'ANDROID_SERIAL':
    return value_string

  # Evaluate the value of the environment variable with string fallback.
  return _eval_value(value_string)

