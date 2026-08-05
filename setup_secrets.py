"""
One-time setup script: creates the Databricks secret scope and stores the
Lakebase connection URL for the ticketing system app.

Run this from a Databricks notebook or locally with the Databricks CLI configured.

Usage:
    Run this entire notebook/script once to set up the secrets.
"""
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import workspace
import getpass

w = WorkspaceClient()

# Create the database secret scope if it doesn't exist
try:
    w.secrets.create_scope(scope="database")
    print("✓ Created 'database' secret scope")
except Exception as e:
    print(f"'database' scope already exists or error: {e}")

# Prompt for the Lakebase connection URL
print("\nEnter your Lakebase Postgres connection URL.")
print("Format: postgresql://username:password@host:5432/databricks_postgres?sslmode=require")
print("\nYou can get this from:")
print("  1. Your Lakebase project endpoint details")
print("  2. Or from your existing secret if already configured")
print("\nExample: postgresql://my_user:my_password@ep-abc-123.us-east-2.aws.neon.tech:5432/databricks_postgres?sslmode=require")

lakebase_url = getpass.getpass("\nPaste your Lakebase URL (input will be hidden): ")

# Store the secret
w.secrets.put_secret(
    scope="database",
    key="lakebase-url",
    string_value=lakebase_url
)
print("✓ Stored Lakebase URL in secrets/database/lakebase-url")

# Grant read access to all users
w.secrets.put_acl(
    scope="database",
    principal="users",
    permission=workspace.AclPermission.READ,
)
print("✓ Granted READ access to 'users' group")

print("\n✅ Setup complete! Your ticketing app should now be able to connect to Lakebase.")
print("\n🔗 App URL: https://lakebase-ticketing-viewer-7474659080524932.aws.databricksapps.com")
