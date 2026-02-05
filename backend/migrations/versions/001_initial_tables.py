"""Initial migration for SIU database

Revision ID: 001_initial_tables
Revises: 
Create Date: 2026-02-04 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = '001_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create roles table first (since users depend on it)
    op.create_table('roles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.Index('ix_roles_name', 'name')
    )

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
        sa.Index('ix_users_username', 'username'),
        sa.Index('ix_users_email', 'email')
    )

    # Create parcels table
    op.create_table('parcels',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('reference_cadastrale', sa.String(), nullable=False),
        sa.Column('coordinates_lat', sa.Float(), nullable=False),
        sa.Column('coordinates_lng', sa.Float(), nullable=False),
        sa.Column('area', sa.Float(), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('geometry', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('owner_id', sa.String(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('cadastral_plan_ref', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('zone', sa.String(), nullable=True),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('province', sa.String(), nullable=True),
        sa.Column('localite', sa.String(), nullable=True),
        sa.Column('realeve', sa.String(), nullable=True),
        sa.Column('reaplanurb', sa.String(), nullable=True),
        sa.Column('reaimplant', sa.String(), nullable=True),
        sa.Column('command', sa.String(), nullable=True),
        sa.Column('numsection', sa.String(), nullable=True),
        sa.Column('numlot', sa.String(), nullable=True),
        sa.Column('numparc', sa.String(), nullable=True),
        sa.Column('commune', sa.String(), nullable=True),
        sa.Column('anneeachev', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('reference_cadastrale'),
        sa.Index('ix_parcels_reference_cadastrale', 'reference_cadastrale'),
        sa.Index('ix_parcels_category', 'category'),
        sa.Index('ix_parcels_owner_id', 'owner_id'),
        sa.Index('ix_parcels_zone', 'zone')
    )

    # Create alerts table
    op.create_table('alerts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('alert_type', sa.Enum('DOUBLE_ATTRIBUTION_ATTEMPT', 'CONFLICT_DETECTED', 'UNAUTHORIZED_ACCESS', 'SUSPICIOUS_ACTIVITY', 'RESERVATION_EXPIRED', name='alerttype'), nullable=False),
        sa.Column('severity', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='alertseverity'), nullable=False),
        sa.Column('parcel_id', sa.String(), nullable=True),
        sa.Column('triggered_by', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('acknowledged', sa.Boolean(), nullable=False),
        sa.Column('acknowledged_by', sa.String(), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['acknowledged_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['parcel_id'], ['parcels.id'], ),
        sa.ForeignKeyConstraint(['triggered_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_alerts_acknowledged', 'acknowledged'),
        sa.Index('ix_alerts_created_at', 'created_at')
    )

    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', sa.String(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('user_role', sa.String(), nullable=True),
        sa.Column('user_ip', sa.String(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('request_method', sa.String(), nullable=True),
        sa.Column('request_path', sa.String(), nullable=True),
        sa.Column('old_data', sa.JSON(), nullable=True),
        sa.Column('new_data', sa.JSON(), nullable=True),
        sa.Column('changes', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('response_status', sa.Integer(), nullable=True),
        sa.Column('is_sensitive', sa.Boolean(), nullable=False),
        sa.Column('requires_review', sa.Boolean(), nullable=False),
        sa.Column('reviewed', sa.Boolean(), nullable=False),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('reviewed_by', sa.String(), nullable=True),
        sa.Column('metadata_ext', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_audit_logs_action', 'action'),
        sa.Index('ix_audit_logs_entity_type', 'entity_type'),
        sa.Index('ix_audit_logs_timestamp', 'timestamp'),
        sa.Index('ix_audit_logs_user_id', 'user_id')
    )

    # Create documents table
    op.create_table('documents',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(), nullable=False),
        sa.Column('parcel_id', sa.String(), nullable=False),
        sa.Column('document_type', sa.Enum('TITLE_DEED', 'SURVEY_PLAN', 'CONTRACT', 'AUTHORIZATION', 'TECHNICAL_DOCUMENT', 'PHOTO', 'TAX_DOCUMENT', 'OTHER', name='documenttype'), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('deleted', sa.Boolean(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('uploaded_by', sa.String(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['parcel_id'], ['parcels.id'], ),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_documents_parcel_id', 'parcel_id')
    )

    # Create parcel_mutations table
    op.create_table('parcel_mutations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('parcel_id', sa.String(), nullable=False),
        sa.Column('mutation_type', sa.Enum('SALE', 'DONATION', 'INHERITANCE', 'EXCHANGE', 'EXPROPRIATION', 'SUBDIVISION', 'MERGE', 'OTHER', name='mutationtype'), nullable=False),
        sa.Column('from_owner_id', sa.String(), nullable=True),
        sa.Column('to_owner_id', sa.String(), nullable=True),
        sa.Column('initiated_by_user_id', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'COMPLETED', 'CANCELLED', name='mutationstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('approved_by_user_id', sa.String(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['approved_by_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['initiated_by_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['parcel_id'], ['parcels.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_parcel_mutations_parcel_id', 'parcel_id'),
        sa.Index('ix_parcel_mutations_status', 'status')
    )

    # Create parcel_history table
    op.create_table('parcel_history',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('parcel_id', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('field', sa.String(), nullable=True),
        sa.Column('old_value', sa.Text(), nullable=True),
        sa.Column('new_value', sa.Text(), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['parcel_id'], ['parcels.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_parcel_history_parcel_id', 'parcel_id'),
        sa.Index('ix_parcel_history_timestamp', 'timestamp')
    )

    # Create zones table
    op.create_table('zones',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('geometry', sa.JSON(), nullable=True),
        sa.Column('zone_type', sa.String(), nullable=True),
        sa.Column('area', sa.Float(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_zones_name', 'name')
    )

    # Create permits table
    op.create_table('permits',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('parcel_id', sa.String(), nullable=False),
        sa.Column('permit_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('applicant_id', sa.String(), nullable=False),
        sa.Column('application_date', sa.DateTime(), nullable=False),
        sa.Column('issue_date', sa.DateTime(), nullable=True),
        sa.Column('expiry_date', sa.DateTime(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('conditions', sa.JSON(), nullable=True),
        sa.Column('fees_paid', sa.Float(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['applicant_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['parcel_id'], ['parcels.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_permits_parcel_id', 'parcel_id'),
        sa.Index('ix_permits_status', 'status')
    )

    # Create parcel_reservations table
    op.create_table('parcel_reservations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('parcel_id', sa.String(), nullable=False),
        sa.Column('reserved_by', sa.String(), nullable=False),
        sa.Column('reservation_date', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('purpose', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['parcel_id'], ['parcels.id'], ),
        sa.ForeignKeyConstraint(['reserved_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_parcel_reservations_parcel_id', 'parcel_id'),
        sa.Index('ix_parcel_reservations_reserved_by', 'reserved_by'),
        sa.Index('ix_parcel_reservations_status', 'status')
    )

    # Create verification_logs table
    op.create_table('verification_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('parcel_id', sa.String(), nullable=False),
        sa.Column('verified_by', sa.String(), nullable=False),
        sa.Column('verification_type', sa.String(), nullable=False),
        sa.Column('result', sa.Boolean(), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['parcel_id'], ['parcels.id'], ),
        sa.ForeignKeyConstraint(['verified_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_verification_logs_parcel_id', 'parcel_id'),
        sa.Index('ix_verification_logs_verified_by', 'verified_by')
    )


def downgrade() -> None:
    # Drop tables in reverse order due to foreign key dependencies
    op.drop_table('verification_logs')
    op.drop_table('parcel_reservations')
    op.drop_table('permits')
    op.drop_table('zones')
    op.drop_table('parcel_history')
    op.drop_table('parcel_mutations')
    op.drop_table('documents')
    op.drop_table('audit_logs')
    op.drop_table('alerts')
    op.drop_table('parcels')
    op.drop_table('users')
    op.drop_table('roles')