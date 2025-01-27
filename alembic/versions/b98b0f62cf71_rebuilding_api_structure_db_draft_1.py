"""rebuilding api structure, db draft 1

Revision ID: b98b0f62cf71
Revises: 06ebefa81a2b
Create Date: 2025-01-19 20:06:36.790230

"""

import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy_utils.types.json import JSONType
from sqlalchemy_utils.types.uuid import UUIDType

from alembic import op
from app.db.custom_types import LongText

# revision identifiers, used by Alembic.
revision = "b98b0f62cf71"
down_revision = "06ebefa81a2b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "platform",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_platform_id"), "platform", ["id"], unique=True)
    op.create_index(op.f("ix_platform_slug"), "platform", ["slug"], unique=True)
    op.create_index(op.f("ix_platform_title"), "platform", ["title"], unique=True)
    op.create_table(
        "client_platform",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("client_id", UUIDType(binary=False), nullable=False),
        sa.Column("platform_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform.id"],
        ),
        sa.PrimaryKeyConstraint("client_id", "platform_id"),
    )
    op.create_index(
        op.f("ix_client_platform_id"), "client_platform", ["id"], unique=True
    )
    op.create_table(
        "client_styleguide",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column("styleguide", JSONType(), nullable=True),
        sa.Column("url", sa.String(length=2048), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("client_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_client_styleguide_id"), "client_styleguide", ["id"], unique=True
    )
    op.create_index(
        op.f("ix_client_styleguide_title"), "client_styleguide", ["title"], unique=True
    )
    op.create_table(
        "go_ads",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("measurement_id", sa.String(length=16), nullable=False),
        sa.Column("platform_id", UUIDType(binary=False), nullable=False),
        sa.Column("client_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"],
            ["platform.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
    )
    op.create_index(op.f("ix_go_ads_id"), "go_ads", ["id"], unique=True)
    op.create_index(
        op.f("ix_go_ads_measurement_id"), "go_ads", ["measurement_id"], unique=True
    )
    op.create_index(op.f("ix_go_ads_title"), "go_ads", ["title"], unique=True)
    op.create_table(
        "website_go_a4",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("website_id", UUIDType(binary=False), nullable=False),
        sa.Column("go_a4_id", UUIDType(binary=False), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["go_a4_id"],
            ["go_a4.id"],
        ),
        sa.ForeignKeyConstraint(
            ["website_id"],
            ["website.id"],
        ),
        sa.PrimaryKeyConstraint("website_id", "go_a4_id"),
    )
    op.create_index(op.f("ix_website_go_a4_id"), "website_go_a4", ["id"], unique=True)
    op.drop_index("ix_client_report_id", table_name="client_report")
    op.drop_index("ix_client_report_title", table_name="client_report")
    op.drop_table("client_report")
    op.drop_index("ix_go_cloud_id", table_name="go_cloud")
    op.drop_index("ix_go_cloud_project_name", table_name="go_cloud")
    op.drop_index("project_id", table_name="go_cloud")
    op.drop_index("project_number", table_name="go_cloud")
    op.drop_index("service_account", table_name="go_cloud")
    op.drop_table("go_cloud")
    op.drop_index("ix_file_asset_caption", table_name="file_asset")
    op.drop_index("ix_file_asset_file_name", table_name="file_asset")
    op.drop_index("ix_file_asset_id", table_name="file_asset")
    op.drop_index("ix_file_asset_title", table_name="file_asset")
    op.drop_table("file_asset")
    op.drop_index("ix_client_report_note_id", table_name="client_report_note")
    op.drop_table("client_report_note")
    op.drop_index("ix_note_id", table_name="note")
    op.drop_index("ix_note_title", table_name="note")
    op.drop_table("note")
    op.drop_index("id", table_name="data_bucket")
    op.drop_index("ix_data_bucket_bucket_name", table_name="data_bucket")
    op.drop_table("data_bucket")
    op.add_column(
        "bdx_feed", sa.Column("platform_id", UUIDType(binary=False), nullable=False)
    )
    op.create_foreign_key(None, "bdx_feed", "platform", ["platform_id"], ["id"])
    op.alter_column(
        "client",
        "description",
        existing_type=mysql.VARCHAR(length=7040),
        type_=sa.String(length=5000),
        existing_nullable=True,
    )
    op.drop_column("client", "style_guide")
    op.drop_constraint("gcft_snap_ibfk_1", "gcft_snap", type_="foreignkey")
    op.drop_column("gcft_snap", "file_asset_id")
    op.alter_column(
        "gcft_snap_hotspotclick",
        "hotspot_content",
        existing_type=mysql.LONGBLOB(),
        type_=LongText(),
        existing_nullable=True,
    )
    op.add_column(
        "go_a4", sa.Column("platform_id", UUIDType(binary=False), nullable=False)
    )
    op.drop_index("ix_go_a4_measurement_id", table_name="go_a4")
    op.create_foreign_key(None, "go_a4", "platform", ["platform_id"], ["id"])
    op.drop_column("go_a4", "measurement_id")
    op.add_column(
        "go_a4_stream",
        sa.Column("measurement_id", sa.String(length=16), nullable=False),
    )
    op.alter_column(
        "go_a4_stream",
        "stream_id",
        existing_type=mysql.VARCHAR(length=408),
        type_=sa.String(length=16),
        existing_nullable=False,
    )
    op.create_index(
        op.f("ix_go_a4_stream_measurement_id"),
        "go_a4_stream",
        ["measurement_id"],
        unique=True,
    )
    op.add_column(
        "go_sc", sa.Column("platform_id", UUIDType(binary=False), nullable=False)
    )
    op.create_foreign_key(None, "go_sc", "platform", ["platform_id"], ["id"])
    op.alter_column(
        "go_sc_country",
        "keys",
        existing_type=mysql.LONGBLOB(),
        type_=LongText(),
        existing_nullable=False,
    )
    op.alter_column(
        "go_sc_device",
        "keys",
        existing_type=mysql.LONGBLOB(),
        type_=LongText(),
        existing_nullable=False,
    )
    op.alter_column(
        "go_sc_page",
        "keys",
        existing_type=mysql.LONGBLOB(),
        type_=LongText(),
        existing_nullable=False,
    )
    op.alter_column(
        "go_sc_query",
        "keys",
        existing_type=mysql.LONGBLOB(),
        type_=LongText(),
        existing_nullable=False,
    )
    op.alter_column(
        "go_sc_searchappearance",
        "keys",
        existing_type=mysql.LONGBLOB(),
        type_=LongText(),
        existing_nullable=False,
    )
    op.add_column(
        "sharpspring", sa.Column("platform_id", UUIDType(binary=False), nullable=False)
    )
    op.create_foreign_key(None, "sharpspring", "platform", ["platform_id"], ["id"])
    op.alter_column(
        "tracking_link",
        "url",
        existing_type=mysql.VARCHAR(length=3116),
        type_=sa.String(length=2048),
        existing_nullable=False,
    )
    op.alter_column(
        "tracking_link",
        "utm_campaign",
        existing_type=mysql.VARCHAR(length=704),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "utm_medium",
        existing_type=mysql.VARCHAR(length=704),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "utm_source",
        existing_type=mysql.VARCHAR(length=704),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "utm_content",
        existing_type=mysql.VARCHAR(length=704),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "utm_term",
        existing_type=mysql.VARCHAR(length=704),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "website_keywordcorpus",
        "corpus",
        existing_type=mysql.LONGBLOB(),
        type_=LongText(),
        existing_nullable=False,
    )
    op.alter_column(
        "website_keywordcorpus",
        "rawtext",
        existing_type=mysql.LONGBLOB(),
        type_=LongText(),
        existing_nullable=False,
    )
    op.alter_column(
        "website_map",
        "url",
        existing_type=mysql.VARCHAR(length=3116),
        type_=sa.String(length=2048),
        existing_nullable=False,
    )
    op.alter_column(
        "website_page",
        "url",
        existing_type=mysql.VARCHAR(length=3116),
        type_=sa.String(length=2048),
        existing_nullable=False,
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("score_grade", sa.Float(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights", sa.Column("grade_data", JSONType(), nullable=False)
    )
    op.drop_column("website_pagespeedinsights", "cls_unit")
    op.drop_column("website_pagespeedinsights", "fcp_grade")
    op.drop_column("website_pagespeedinsights", "ps_unit")
    op.drop_column("website_pagespeedinsights", "cls_grade")
    op.drop_column("website_pagespeedinsights", "fcp_value")
    op.drop_column("website_pagespeedinsights", "ps_grade")
    op.drop_column("website_pagespeedinsights", "si_grade")
    op.drop_column("website_pagespeedinsights", "ps_weight")
    op.drop_column("website_pagespeedinsights", "si_weight")
    op.drop_column("website_pagespeedinsights", "cls_weight")
    op.drop_column("website_pagespeedinsights", "si_value")
    op.drop_column("website_pagespeedinsights", "si_unit")
    op.drop_column("website_pagespeedinsights", "cls_value")
    op.drop_column("website_pagespeedinsights", "tbt_unit")
    op.drop_column("website_pagespeedinsights", "lcp_unit")
    op.drop_column("website_pagespeedinsights", "fcp_unit")
    op.drop_column("website_pagespeedinsights", "tbt_grade")
    op.drop_column("website_pagespeedinsights", "lcp_value")
    op.drop_column("website_pagespeedinsights", "ps_value")
    op.drop_column("website_pagespeedinsights", "fcp_weight")
    op.drop_column("website_pagespeedinsights", "tbt_value")
    op.drop_column("website_pagespeedinsights", "lcp_weight")
    op.drop_column("website_pagespeedinsights", "lcp_grade")
    op.drop_column("website_pagespeedinsights", "tbt_weight")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("tbt_weight", mysql.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("lcp_grade", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("lcp_weight", mysql.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("tbt_value", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("fcp_weight", mysql.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("ps_value", mysql.VARCHAR(length=408), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("lcp_value", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("tbt_grade", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("fcp_unit", mysql.VARCHAR(length=408), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("lcp_unit", mysql.VARCHAR(length=408), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("tbt_unit", mysql.VARCHAR(length=408), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("cls_value", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("si_unit", mysql.VARCHAR(length=408), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("si_value", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("cls_weight", mysql.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("si_weight", mysql.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("ps_weight", mysql.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("si_grade", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("ps_grade", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("fcp_value", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("cls_grade", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("ps_unit", mysql.VARCHAR(length=408), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("fcp_grade", mysql.FLOAT(), nullable=False),
    )
    op.add_column(
        "website_pagespeedinsights",
        sa.Column("cls_unit", mysql.VARCHAR(length=408), nullable=False),
    )
    op.drop_column("website_pagespeedinsights", "grade_data")
    op.drop_column("website_pagespeedinsights", "score_grade")
    op.alter_column(
        "website_page",
        "url",
        existing_type=sa.String(length=2048),
        type_=mysql.VARCHAR(length=3116),
        existing_nullable=False,
    )
    op.alter_column(
        "website_map",
        "url",
        existing_type=sa.String(length=2048),
        type_=mysql.VARCHAR(length=3116),
        existing_nullable=False,
    )
    op.alter_column(
        "website_keywordcorpus",
        "rawtext",
        existing_type=LongText(),
        type_=mysql.LONGBLOB(),
        existing_nullable=False,
    )
    op.alter_column(
        "website_keywordcorpus",
        "corpus",
        existing_type=LongText(),
        type_=mysql.LONGBLOB(),
        existing_nullable=False,
    )
    op.alter_column(
        "tracking_link",
        "utm_term",
        existing_type=sa.String(length=255),
        type_=mysql.VARCHAR(length=704),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "utm_content",
        existing_type=sa.String(length=255),
        type_=mysql.VARCHAR(length=704),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "utm_source",
        existing_type=sa.String(length=255),
        type_=mysql.VARCHAR(length=704),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "utm_medium",
        existing_type=sa.String(length=255),
        type_=mysql.VARCHAR(length=704),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "utm_campaign",
        existing_type=sa.String(length=255),
        type_=mysql.VARCHAR(length=704),
        existing_nullable=True,
    )
    op.alter_column(
        "tracking_link",
        "url",
        existing_type=sa.String(length=2048),
        type_=mysql.VARCHAR(length=3116),
        existing_nullable=False,
    )
    op.drop_constraint(None, "sharpspring", type_="foreignkey")
    op.drop_column("sharpspring", "platform_id")
    op.alter_column(
        "go_sc_searchappearance",
        "keys",
        existing_type=LongText(),
        type_=mysql.LONGBLOB(),
        existing_nullable=False,
    )
    op.alter_column(
        "go_sc_query",
        "keys",
        existing_type=LongText(),
        type_=mysql.LONGBLOB(),
        existing_nullable=False,
    )
    op.alter_column(
        "go_sc_page",
        "keys",
        existing_type=LongText(),
        type_=mysql.LONGBLOB(),
        existing_nullable=False,
    )
    op.alter_column(
        "go_sc_device",
        "keys",
        existing_type=LongText(),
        type_=mysql.LONGBLOB(),
        existing_nullable=False,
    )
    op.alter_column(
        "go_sc_country",
        "keys",
        existing_type=LongText(),
        type_=mysql.LONGBLOB(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "go_sc", type_="foreignkey")
    op.drop_column("go_sc", "platform_id")
    op.drop_index(op.f("ix_go_a4_stream_measurement_id"), table_name="go_a4_stream")
    op.alter_column(
        "go_a4_stream",
        "stream_id",
        existing_type=sa.String(length=16),
        type_=mysql.VARCHAR(length=408),
        existing_nullable=False,
    )
    op.drop_column("go_a4_stream", "measurement_id")
    op.add_column(
        "go_a4", sa.Column("measurement_id", mysql.VARCHAR(length=16), nullable=False)
    )
    op.drop_constraint(None, "go_a4", type_="foreignkey")
    op.create_index("ix_go_a4_measurement_id", "go_a4", ["measurement_id"], unique=True)
    op.drop_column("go_a4", "platform_id")
    op.alter_column(
        "gcft_snap_hotspotclick",
        "hotspot_content",
        existing_type=LongText(),
        type_=mysql.LONGBLOB(),
        existing_nullable=True,
    )
    op.add_column(
        "gcft_snap", sa.Column("file_asset_id", mysql.CHAR(length=32), nullable=True)
    )
    op.create_foreign_key(
        "gcft_snap_ibfk_1", "gcft_snap", "file_asset", ["file_asset_id"], ["id"]
    )
    op.add_column("client", sa.Column("style_guide", mysql.TEXT(), nullable=True))
    op.alter_column(
        "client",
        "description",
        existing_type=sa.String(length=5000),
        type_=mysql.VARCHAR(length=7040),
        existing_nullable=True,
    )
    op.drop_constraint(None, "bdx_feed", type_="foreignkey")
    op.drop_column("bdx_feed", "platform_id")
    op.create_table(
        "data_bucket",
        sa.Column("id", mysql.CHAR(length=32), nullable=False),
        sa.Column("bucket_name", mysql.VARCHAR(length=63), nullable=False),
        sa.Column("bucket_prefix", mysql.VARCHAR(length=769), nullable=False),
        sa.Column("description", mysql.VARCHAR(length=7040), nullable=True),
        sa.Column("client_id", mysql.CHAR(length=32), nullable=True),
        sa.Column("bdx_feed_id", mysql.CHAR(length=32), nullable=True),
        sa.Column("gcft_id", mysql.CHAR(length=32), nullable=True),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.Column("updated", mysql.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bdx_feed_id"], ["bdx_feed.id"], name="data_bucket_ibfk_1"
        ),
        sa.ForeignKeyConstraint(
            ["client_id"], ["client.id"], name="data_bucket_ibfk_2"
        ),
        sa.ForeignKeyConstraint(["gcft_id"], ["gcft.id"], name="data_bucket_ibfk_3"),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index(
        "ix_data_bucket_bucket_name", "data_bucket", ["bucket_name"], unique=False
    )
    op.create_index("id", "data_bucket", ["id"], unique=True)
    op.create_table(
        "note",
        sa.Column("id", mysql.CHAR(length=32), nullable=False),
        sa.Column("title", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("description", mysql.VARCHAR(length=7040), nullable=False),
        sa.Column("is_active", mysql.VARCHAR(length=428), nullable=False),
        sa.Column("user_id", mysql.CHAR(length=32), nullable=False),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.Column("updated", mysql.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name="note_ibfk_1"),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("ix_note_title", "note", ["title"], unique=True)
    op.create_index("ix_note_id", "note", ["id"], unique=True)
    op.create_table(
        "client_report_note",
        sa.Column("id", mysql.CHAR(length=32), nullable=False),
        sa.Column("client_report_id", mysql.CHAR(length=32), nullable=False),
        sa.Column("note_id", mysql.CHAR(length=32), nullable=False),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.Column("updated", mysql.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_report_id"], ["client_report.id"], name="client_report_note_ibfk_1"
        ),
        sa.ForeignKeyConstraint(
            ["note_id"], ["note.id"], name="client_report_note_ibfk_2"
        ),
        sa.PrimaryKeyConstraint("client_report_id", "note_id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index(
        "ix_client_report_note_id", "client_report_note", ["id"], unique=True
    )
    op.create_table(
        "file_asset",
        sa.Column("id", mysql.CHAR(length=32), nullable=False),
        sa.Column("file_name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("mime_type", mysql.VARCHAR(length=1024), nullable=False),
        sa.Column("size_kb", mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("title", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("caption", mysql.VARCHAR(length=255), nullable=True),
        sa.Column("user_id", mysql.CHAR(length=32), nullable=False),
        sa.Column("client_id", mysql.CHAR(length=32), nullable=False),
        sa.Column("geocoord_id", mysql.CHAR(length=32), nullable=True),
        sa.Column("bdx_feed_id", mysql.CHAR(length=32), nullable=True),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.Column("updated", mysql.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bdx_feed_id"], ["bdx_feed.id"], name="file_asset_ibfk_1"
        ),
        sa.ForeignKeyConstraint(["client_id"], ["client.id"], name="file_asset_ibfk_2"),
        sa.ForeignKeyConstraint(
            ["geocoord_id"], ["geocoord.id"], name="file_asset_ibfk_3"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name="file_asset_ibfk_4"),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("ix_file_asset_title", "file_asset", ["title"], unique=False)
    op.create_index("ix_file_asset_id", "file_asset", ["id"], unique=True)
    op.create_index("ix_file_asset_file_name", "file_asset", ["file_name"], unique=True)
    op.create_index("ix_file_asset_caption", "file_asset", ["caption"], unique=False)
    op.create_table(
        "go_cloud",
        sa.Column("id", mysql.CHAR(length=32), nullable=False),
        sa.Column("project_name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("project_id", mysql.VARCHAR(length=472), nullable=False),
        sa.Column("project_number", mysql.VARCHAR(length=472), nullable=False),
        sa.Column("service_account", mysql.VARCHAR(length=704), nullable=True),
        sa.Column("client_id", mysql.CHAR(length=32), nullable=False),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.Column("updated", mysql.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["client.id"], name="go_cloud_ibfk_1"),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("service_account", "go_cloud", ["service_account"], unique=True)
    op.create_index("project_number", "go_cloud", ["project_number"], unique=True)
    op.create_index("project_id", "go_cloud", ["project_id"], unique=True)
    op.create_index(
        "ix_go_cloud_project_name", "go_cloud", ["project_name"], unique=True
    )
    op.create_index("ix_go_cloud_id", "go_cloud", ["id"], unique=True)
    op.create_table(
        "client_report",
        sa.Column("id", mysql.CHAR(length=32), nullable=False),
        sa.Column("title", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("url", mysql.VARCHAR(length=2048), nullable=False),
        sa.Column("description", mysql.VARCHAR(length=7040), nullable=True),
        sa.Column("keys", mysql.LONGBLOB(), nullable=True),
        sa.Column("client_id", mysql.CHAR(length=32), nullable=False),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.Column("updated", mysql.DATETIME(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"], ["client.id"], name="client_report_ibfk_1"
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("ix_client_report_title", "client_report", ["title"], unique=True)
    op.create_index("ix_client_report_id", "client_report", ["id"], unique=True)
    op.drop_index(op.f("ix_website_go_a4_id"), table_name="website_go_a4")
    op.drop_table("website_go_a4")
    op.drop_index(op.f("ix_go_ads_title"), table_name="go_ads")
    op.drop_index(op.f("ix_go_ads_measurement_id"), table_name="go_ads")
    op.drop_index(op.f("ix_go_ads_id"), table_name="go_ads")
    op.drop_table("go_ads")
    op.drop_index(op.f("ix_client_styleguide_title"), table_name="client_styleguide")
    op.drop_index(op.f("ix_client_styleguide_id"), table_name="client_styleguide")
    op.drop_table("client_styleguide")
    op.drop_index(op.f("ix_client_platform_id"), table_name="client_platform")
    op.drop_table("client_platform")
    op.drop_index(op.f("ix_platform_title"), table_name="platform")
    op.drop_index(op.f("ix_platform_slug"), table_name="platform")
    op.drop_index(op.f("ix_platform_id"), table_name="platform")
    op.drop_table("platform")
    # ### end Alembic commands ###