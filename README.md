
# Django Sync

**Django Sync** is a powerful Django utility that enables seamless data synchronization between two databases. It is designed to be simple to configure and flexible to use, supporting both manual and automatic synchronization.

## Features

*   **Directional Sync:** Synchronize data from a `default` database to a `slave` database, or vice-versa.
*   **Manual Sync Command:** A `sync_data` management command with directional control.
*   **Automatic Sync:** Automatically syncs data on model save and delete operations.
*   **Flexible Configuration:** Easily configure which models and fields to include or exclude from synchronization.

## Installation

1.  Install the package from PyPI:

    ```bash
    pip install django-sync-package
    ```

2.  Add `'sync'` to your `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = [
        # ... other apps
        'sync',
    ]
    ```

## Configuration

1.  **Databases:** In your `settings.py`, define your `default` (master) database and a `slave` database connection.

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_master',
            # ... other settings
        },
        'slave': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_slave',
            # ... other settings
        }
    }
    ```

2.  **Sync Configuration:** Add a `SYNC_CONFIG` dictionary to your `settings.py` to specify which models to sync.

    ```python
    SYNC_CONFIG = {
        'MODELS': [
            'auth.User',
            'yourapp.YourModel',
        ],
        'EXCLUDE': {
            'auth.User': ['password', 'last_login', 'date_joined'],
        }
    }
    ```

## Usage

### Manual Synchronization

The `sync_data` management command allows you to perform a uni-directional sync. You can control the direction with the `--direction` flag.

*   **Push data from `default` to `slave`:**

    ```bash
    python manage.py sync_data --direction=master-to-slave
    ```

*   **Pull data from `slave` to `default`:**

    ```bash
    python manage.py sync_data --direction=slave-to-master
    ```

#### Example: Syncing Two Instances

If you are running two separate instances of a project (e.g., on different servers), you can keep them in sync by configuring each instance to recognize the other's database and running a two-step sync process:

1.  **Pull changes from the remote instance:** `python manage.py sync_data --direction=slave-to-master`
2.  **Push local changes to the remote instance:** `python manage.py sync_data --direction=master-to-slave`

### Automatic Synchronization

By default, **Django Sync** will automatically trigger a synchronization whenever a model included in `SYNC_CONFIG` is saved or deleted.

*   When an object is created, updated, or deleted in the `default` database, the change is automatically propagated to the `slave` database.
*   This provides a simple way to maintain a real-time replica of your data.

## Running Tests

To run the built-in tests for the `sync` app:

```bash
python manage.py test sync
```

## Contributing

Contributions are welcome! If you have a feature request, bug report, or a pull request, please feel free to open an issue or submit a PR on the project's GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
