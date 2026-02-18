"""初始化Alembic迁移"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

def upgrade() -> None:
    """创建所有表"""
    
    # 创建users表
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_username', 'users', ['username'])
    
    # 创建destinations表
    op.create_table(
        'destinations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('name_en', sa.String(200), nullable=True),
        sa.Column('country', sa.String(100), nullable=False),
        sa.Column('province', sa.String(100), nullable=True),
        sa.Column('city', sa.String(100), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(500), nullable=True),
        sa.Column('best_season', sa.String(50), nullable=True),
        sa.Column('suggested_days', sa.Integer(), nullable=True),
        sa.Column('avg_budget', sa.Integer(), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('popularity_score', sa.Float(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'city', name='uq_destination_name_city')
    )
    op.create_index('ix_destinations_city', 'destinations', ['city'])
    op.create_index('ix_destinations_country', 'destinations', ['country'])
    op.create_index('ix_destinations_rating', 'destinations', ['rating'])
    op.create_index('ix_destinations_popularity', 'destinations', ['popularity_score'])
    
    # 创建attractions表
    op.create_table(
        'attractions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('destination_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('review_count', sa.Integer(), nullable=True),
        sa.Column('ticket_price', sa.Float(), nullable=True),
        sa.Column('opening_hours', sa.JSON(), nullable=True),
        sa.Column('recommended_duration', sa.Integer(), nullable=True),
        sa.Column('best_time_to_visit', sa.String(100), nullable=True),
        sa.Column('image_urls', sa.JSON(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['destination_id'], ['destinations.id'], )
    )
    op.create_index('ix_attractions_destination_id', 'attractions', ['destination_id'])
    op.create_index('ix_attractions_rating', 'attractions', ['rating'])
    op.create_index('ix_attractions_category', 'attractions', ['category'])
    
    # 创建restaurants表
    op.create_table(
        'restaurants',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('destination_id', sa.Integer(), nullable=False),
        sa.Column('cuisine_type', sa.String(100), nullable=True),
        sa.Column('price_level', sa.Integer(), nullable=True),
        sa.Column('avg_price_per_person', sa.Float(), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('review_count', sa.Integer(), nullable=True),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('opening_hours', sa.JSON(), nullable=True),
        sa.Column('specialties', sa.JSON(), nullable=True),
        sa.Column('image_urls', sa.JSON(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['destination_id'], ['destinations.id'], )
    )
    op.create_index('ix_restaurants_destination_id', 'restaurants', ['destination_id'])
    op.create_index('ix_restaurants_rating', 'restaurants', ['rating'])
    op.create_index('ix_restaurants_cuisine_type', 'restaurants', ['cuisine_type'])
    op.create_index('ix_restaurants_price_level', 'restaurants', ['price_level'])
    
    # 创建itineraries表
    op.create_table(
        'itineraries',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('days', sa.Integer(), nullable=False),
        sa.Column('total_budget', sa.Float(), nullable=True),
        sa.Column('actual_cost', sa.Float(), nullable=True),
        sa.Column('plan_type', sa.String(50), nullable=True),
        sa.Column('destinations', sa.JSON(), nullable=True),
        sa.Column('daily_schedule', sa.JSON(), nullable=True),
        sa.Column('transportation', sa.JSON(), nullable=True),
        sa.Column('accommodation', sa.JSON(), nullable=True),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_index('ix_itineraries_user_id', 'itineraries', ['user_id'])
    op.create_index('ix_itineraries_status', 'itineraries', ['status'])


def downgrade() -> None:
    """删除所有表"""
    op.drop_index('ix_itineraries_status', table_name='itineraries')
    op.drop_index('ix_itineraries_user_id', table_name='itineraries')
    op.drop_table('itineraries')
    
    op.drop_index('ix_restaurants_price_level', table_name='restaurants')
    op.drop_index('ix_restaurants_cuisine_type', table_name='restaurants')
    op.drop_index('ix_restaurants_rating', table_name='restaurants')
    op.drop_index('ix_restaurants_destination_id', table_name='restaurants')
    op.drop_table('restaurants')
    
    op.drop_index('ix_attractions_category', table_name='attractions')
    op.drop_index('ix_attractions_rating', table_name='attractions')
    op.drop_index('ix_attractions_destination_id', table_name='attractions')
    op.drop_table('attractions')
    
    op.drop_index('ix_destinations_popularity', table_name='destinations')
    op.drop_index('ix_destinations_rating', table_name='destinations')
    op.drop_index('ix_destinations_country', table_name='destinations')
    op.drop_index('ix_destinations_city', table_name='destinations')
    op.drop_table('destinations')
    
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
