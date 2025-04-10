import os


def get_auth_token() -> str:
    """
    Retrieves the Synapse authentication token from the user's ~/.synapseConfig file.

    The config file is expected to contain a line in the format:
      authtoken = <token>
    See the README for information on how to set this up.

    :return: The authentication token found in the config file.
    :raises:
      FileNotFoundError: If the ~/.synapseConfig file does not exist
      ValueError: If the 'authtoken' line is missing, malformed, or empty
      RuntimeError: If an unexpected error occurs while reading the file.
    """
    auth_file = os.path.expanduser("~/.synapseConfig")

    try:
        with open(auth_file, "r") as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line.startswith("authtoken"):
                    key, value = map(str.strip, stripped_line.split("=", 1))
                    if key == "authtoken" and value:
                        return value
                    else:
                        raise ValueError("The 'authtoken' line is malformed or empty.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Authentication file not found: {auth_file}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the auth file: {e}")

    raise ValueError(f"'authtoken' not found in {auth_file}")
