/* CREATE THE DATABASE AND APPROPRIATE SCHEMAS */
DROP DATABASE IF EXISTS job_tracking_dev
GO

CREATE DATABASE job_tracking_dev
GO

CREATE SCHEMA quoting_system_db
GO

CREATE SCHEMA hr_system
GO

CREATE SCHEMA integrations
GO

CREATE SCHEMA production_system;
GO

CREATE SCHEMA quality_system
GO

CREATE SCHEMA security_system
GO

CREATE SCHEMA report_system
GO

/****** Object:  Table [quoting_system_db].[branch]    Script Date: 18/09/2024 1:43:00 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [quoting_system_db].[branch](
	[branch_name] [nvarchar](50) NOT NULL,
	[branch_guid] [uniqueidentifier] NULL,
 CONSTRAINT [PK_branch_branch_name] PRIMARY KEY CLUSTERED 
(
	[branch_name] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [quoting_system_db].[branch] ADD  CONSTRAINT [df_branch_guid]  DEFAULT (newid()) FOR [branch_guid]
GO

/****** Object:  Table [hr_system].[resource_group_category]    Script Date: 19/09/2024 11:39:52 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [hr_system].[resource_group_category](
	[group_category_name] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_resource_group_category] PRIMARY KEY CLUSTERED 
(
	[group_category_name] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [hr_system].[resource_group]    Script Date: 18/09/2024 1:55:21 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [hr_system].[resource_group](
	[group_id] [int] IDENTITY(10000,1) NOT NULL,
	[group_name] [nvarchar](50) NOT NULL,
	[group_parent_group] [int] NULL,
	[group_category_name] [nvarchar](50) NULL,
 CONSTRAINT [PK_resource_group] PRIMARY KEY CLUSTERED 
(
	[group_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [hr_system].[resource_group] ADD  CONSTRAINT [DF_resource_group_group_category_name]  DEFAULT (N'Uncategorised') FOR [group_category_name]
GO

ALTER TABLE [hr_system].[resource_group]  WITH CHECK ADD  CONSTRAINT [FK_resource_group_resource_group] FOREIGN KEY([group_parent_group])
REFERENCES [hr_system].[resource_group] ([group_id])
GO

ALTER TABLE [hr_system].[resource_group] CHECK CONSTRAINT [FK_resource_group_resource_group]
GO

ALTER TABLE [hr_system].[resource_group]  WITH CHECK ADD  CONSTRAINT [FK_resource_group_resource_group_category] FOREIGN KEY([group_category_name])
REFERENCES [hr_system].[resource_group_category] ([group_category_name])
GO

ALTER TABLE [hr_system].[resource_group] CHECK CONSTRAINT [FK_resource_group_resource_group_category]
GO

/****** Object:  Table [quoting_system_db].[contact]    Script Date: 18/09/2024 3:13:49 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [quoting_system_db].[contact](
	[contact_id] [int] IDENTITY(1,1) NOT NULL,
	[contact_first_name] [nvarchar](255) NOT NULL,
	[contact_last_name] [nvarchar](255) NULL,
	[contact_pref_name] [nvarchar](100) NULL,
 CONSTRAINT [PK_contact] PRIMARY KEY CLUSTERED 
(
	[contact_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [hr_system].[human_resource]    Script Date: 18/09/2024 2:51:40 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [hr_system].[human_resource](
	[hr_id] [int] IDENTITY(10000,1) NOT NULL,
	[hr_job_title] [nvarchar](100) NOT NULL,
	[contact_id] [int] NOT NULL,
	[hr_supervisor_id] [int] NULL,
	[branch_name] [nvarchar](50) NULL,
	[hr_guid] [uniqueidentifier] NULL,
	[hr_pin] [nvarchar](32) NULL,
	[hr_timesheet_user] [bit] NULL,
 CONSTRAINT [PK_human_resource] PRIMARY KEY CLUSTERED 
(
	[hr_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [UC_hr_guid] UNIQUE NONCLUSTERED 
(
	[hr_guid] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [hr_system].[human_resource] ADD  DEFAULT (newid()) FOR [hr_guid]
GO

ALTER TABLE [hr_system].[human_resource] ADD  CONSTRAINT [DF_human_resource_hr_timesheet_user]  DEFAULT ((0)) FOR [hr_timesheet_user]
GO

ALTER TABLE [hr_system].[human_resource]  WITH CHECK ADD  CONSTRAINT [FK_human_resource_branch] FOREIGN KEY([branch_name])
REFERENCES [quoting_system_db].[branch] ([branch_name])
ON UPDATE CASCADE
GO

ALTER TABLE [hr_system].[human_resource] CHECK CONSTRAINT [FK_human_resource_branch]
GO

ALTER TABLE [hr_system].[human_resource]  WITH CHECK ADD  CONSTRAINT [FK_human_resource_contact] FOREIGN KEY([contact_id])
REFERENCES [quoting_system_db].[contact] ([contact_id])
ON UPDATE CASCADE
GO

ALTER TABLE [hr_system].[human_resource] CHECK CONSTRAINT [FK_human_resource_contact]
GO

ALTER TABLE [hr_system].[human_resource]  WITH CHECK ADD  CONSTRAINT [FK_human_resource_human_resource] FOREIGN KEY([hr_supervisor_id])
REFERENCES [hr_system].[human_resource] ([hr_id])
GO

ALTER TABLE [hr_system].[human_resource] CHECK CONSTRAINT [FK_human_resource_human_resource]
GO

/****** Object:  Table [integrations].[asana_operations_project]    Script Date: 19/09/2024 9:23:03 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [integrations].[asana_operations_project](
	[project_gid] [nvarchar](50) NOT NULL,
	[is_worklist] [bit] NULL,
	[worklist_complete] [nvarchar](100) NULL,
	[worklist_yes] [nvarchar](100) NULL,
	[worklist_no] [nvarchar](100) NULL,
	[worklist_in_progress] [nvarchar](100) NULL,
 CONSTRAINT [PK_asana_operations_project] PRIMARY KEY CLUSTERED 
(
	[project_gid] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [integrations].[asana_project_resource_group]    Script Date: 19/09/2024 9:16:47 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [integrations].[asana_project_resource_group](
	[resource_group_id] [int] NOT NULL,
	[asana_project_gid] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_asana_project_resource_group] PRIMARY KEY CLUSTERED 
(
	[resource_group_id] ASC,
	[asana_project_gid] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [integrations].[asana_project_resource_group]  WITH CHECK ADD  CONSTRAINT [FK_asana_project_resource_group_resource_group] FOREIGN KEY([resource_group_id])
REFERENCES [hr_system].[resource_group] ([group_id])
GO

ALTER TABLE [integrations].[asana_project_resource_group] CHECK CONSTRAINT [FK_asana_project_resource_group_resource_group]
GO

ALTER TABLE [integrations].[asana_project_resource_group]  WITH CHECK ADD  CONSTRAINT [FK_asana_project_resource_group_asana_project] FOREIGN KEY([asana_project_gid])
REFERENCES [integrations].[asana_operations_project] ([project_gid])
GO

ALTER TABLE [integrations].[asana_project_resource_group] CHECK CONSTRAINT [FK_asana_project_resource_group_asana_project]
GO

/****** Object:  Table [integrations].[asana_task]    Script Date: 19/09/2024 9:15:51 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [integrations].[asana_task](
	[task_name] [nvarchar](250) NOT NULL,
	[task_gid] [nvarchar](50) NOT NULL,
	[stair_category] [nvarchar](50) NULL,
 CONSTRAINT [PK_asana_unscheduled_job] PRIMARY KEY CLUSTERED 
(
	[task_gid] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [production_system].[job_tracking_entry]    Script Date: 19/09/2024 9:52:52 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [production_system].[job_tracking_entry](
	[entry_id] [int] IDENTITY(10000,1) NOT NULL,
	[entry_date] [date] NOT NULL,
	[entry_branch_name] [nvarchar](50) NOT NULL,
	[entry_area_group_id] [int] NOT NULL,
	[entry_hr_id] [int] NOT NULL,
	[entry_job_id] [int] NULL,
	[entry_task_gid] [nvarchar](50) NOT NULL,
	[entry_start_time] [datetime] NOT NULL,
	[entry_end_time] [datetime] NULL,
	[entry_comment] [nvarchar](max) NULL,
 CONSTRAINT [PK_job_tracking_entry] PRIMARY KEY CLUSTERED 
(
	[entry_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [production_system].[job_tracking_entry] ADD  CONSTRAINT [DF_job_tracking_entry_entry_date]  DEFAULT (getdate()) FOR [entry_date]
GO

ALTER TABLE [production_system].[job_tracking_entry]  WITH CHECK ADD  CONSTRAINT [FK_job_tracking_entry_branch] FOREIGN KEY([entry_branch_name])
REFERENCES [quoting_system_db].[branch] ([branch_name])
ON UPDATE CASCADE
GO

ALTER TABLE [production_system].[job_tracking_entry] CHECK CONSTRAINT [FK_job_tracking_entry_branch]
GO

ALTER TABLE [production_system].[job_tracking_entry]  WITH CHECK ADD  CONSTRAINT [FK_job_tracking_entry_human_resource] FOREIGN KEY([entry_hr_id])
REFERENCES [hr_system].[human_resource] ([hr_id])
GO

ALTER TABLE [production_system].[job_tracking_entry] CHECK CONSTRAINT [FK_job_tracking_entry_human_resource]
GO

ALTER TABLE [production_system].[job_tracking_entry]  WITH CHECK ADD  CONSTRAINT [FK_job_tracking_entry_resource_group] FOREIGN KEY([entry_area_group_id])
REFERENCES [hr_system].[resource_group] ([group_id])
GO

ALTER TABLE [production_system].[job_tracking_entry] CHECK CONSTRAINT [FK_job_tracking_entry_resource_group]
GO

/****** Object:  Table [production_system].[job_tracking_entry_image]    Script Date: 19/09/2024 10:41:37 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [production_system].[job_tracking_entry_image](
	[entry_image_id] [int] IDENTITY(100000,1) NOT NULL,
	[entry_id] [int] NOT NULL,
	[entry_image_url] [nvarchar](max) NOT NULL,
 CONSTRAINT [PK_job_tracking_entry_image] PRIMARY KEY CLUSTERED 
(
	[entry_image_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [production_system].[job_tracking_entry_image]  WITH CHECK ADD  CONSTRAINT [FK_job_tracking_entry_job_tracking_entry_image] FOREIGN KEY([entry_id])
REFERENCES [production_system].[job_tracking_entry] ([entry_id])
ON UPDATE CASCADE
GO

ALTER TABLE [production_system].[job_tracking_entry_image] CHECK CONSTRAINT [FK_job_tracking_entry_job_tracking_entry_image]
GO

/****** Object:  Table [quality_system].[error]    Script Date: 19/09/2024 10:54:32 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [quality_system].[error](
	[error_id] [int] IDENTITY(1000,1) NOT NULL,
	[error_desc] [nvarchar](max) NOT NULL,
	[error_department] [int] NOT NULL,
 CONSTRAINT [PK_error] PRIMARY KEY CLUSTERED 
(
	[error_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [quality_system].[error]  WITH CHECK ADD  CONSTRAINT [FK_error_resource_group] FOREIGN KEY([error_department])
REFERENCES [hr_system].[resource_group] ([group_id])
ON UPDATE CASCADE
GO

ALTER TABLE [quality_system].[error] CHECK CONSTRAINT [FK_error_resource_group]
GO

/****** Object:  Table [quality_system].[error_group]    Script Date: 19/09/2024 10:54:42 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [quality_system].[error_group](
	[error_group_id] [int] IDENTITY(1000,1) NOT NULL,
	[error_group_name] [nvarchar](100) NOT NULL,
 CONSTRAINT [PK_error_group] PRIMARY KEY CLUSTERED 
(
	[error_group_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [U_error_group_name] UNIQUE NONCLUSTERED 
(
	[error_group_name] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [quality_system].[error_group_error]    Script Date: 19/09/2024 10:54:52 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [quality_system].[error_group_error](
	[error_group_id] [int] NOT NULL,
	[error_id] [int] NOT NULL,
 CONSTRAINT [PK_error_group_error] PRIMARY KEY CLUSTERED 
(
	[error_group_id] ASC,
	[error_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [quality_system].[error_group_error]  WITH CHECK ADD  CONSTRAINT [FK_error_group_error_error] FOREIGN KEY([error_id])
REFERENCES [quality_system].[error] ([error_id])
GO

ALTER TABLE [quality_system].[error_group_error] CHECK CONSTRAINT [FK_error_group_error_error]
GO

ALTER TABLE [quality_system].[error_group_error]  WITH CHECK ADD  CONSTRAINT [FK_error_group_error_error_group] FOREIGN KEY([error_group_id])
REFERENCES [quality_system].[error_group] ([error_group_id])
GO

ALTER TABLE [quality_system].[error_group_error] CHECK CONSTRAINT [FK_error_group_error_error_group]
GO

/****** Object:  Table [report_system].[error_report]    Script Date: 19/09/2024 10:55:07 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [report_system].[error_report](
	[error_report_id] [int] IDENTITY(100000,1) NOT NULL,
	[reported_at_department] [int] NOT NULL,
	[hr_id] [int] NOT NULL,
	[task_gid] [nvarchar](50) NOT NULL,
	[reported_at_time] [datetime] NOT NULL,
	[comments] [nvarchar](max) NULL,
 CONSTRAINT [PK_error_report] PRIMARY KEY CLUSTERED 
(
	[error_report_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [report_system].[error_report] ADD  CONSTRAINT [DF_error_report_reported_at_time]  DEFAULT (getdate()) FOR [reported_at_time]
GO

ALTER TABLE [report_system].[error_report]  WITH CHECK ADD  CONSTRAINT [FK_error_report_human_resource] FOREIGN KEY([hr_id])
REFERENCES [hr_system].[human_resource] ([hr_id])
GO

ALTER TABLE [report_system].[error_report] CHECK CONSTRAINT [FK_error_report_human_resource]
GO

ALTER TABLE [report_system].[error_report]  WITH CHECK ADD  CONSTRAINT [FK_error_report_job] FOREIGN KEY([task_gid])
REFERENCES [integrations].[asana_task] ([task_gid])
GO

ALTER TABLE [report_system].[error_report] CHECK CONSTRAINT [FK_error_report_job]
GO

ALTER TABLE [report_system].[error_report]  WITH CHECK ADD  CONSTRAINT [FK_error_report_resource_group] FOREIGN KEY([reported_at_department])
REFERENCES [hr_system].[resource_group] ([group_id])
GO

ALTER TABLE [report_system].[error_report] CHECK CONSTRAINT [FK_error_report_resource_group]
GO

/****** Object:  Table [report_system].[error_report_error]    Script Date: 19/09/2024 10:55:16 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [report_system].[error_report_error](
	[error_report_id] [int] NOT NULL,
	[error_id] [int] NOT NULL,
 CONSTRAINT [PK_error_report_error] PRIMARY KEY CLUSTERED 
(
	[error_report_id] ASC,
	[error_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [report_system].[error_report_error]  WITH CHECK ADD  CONSTRAINT [FK_error_report_error_error] FOREIGN KEY([error_id])
REFERENCES [quality_system].[error] ([error_id])
GO

ALTER TABLE [report_system].[error_report_error] CHECK CONSTRAINT [FK_error_report_error_error]
GO

ALTER TABLE [report_system].[error_report_error]  WITH CHECK ADD  CONSTRAINT [FK_error_report_error_error_report] FOREIGN KEY([error_report_id])
REFERENCES [report_system].[error_report] ([error_report_id])
GO

ALTER TABLE [report_system].[error_report_error] CHECK CONSTRAINT [FK_error_report_error_error_report]
GO

/****** Object:  Table [report_system].[error_report_image]    Script Date: 19/09/2024 10:55:23 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [report_system].[error_report_image](
	[error_report_image_id] [int] IDENTITY(1000,1) NOT NULL,
	[error_report_id] [int] NOT NULL,
	[image_url] [nvarchar](max) NOT NULL,
 CONSTRAINT [PK_error_report_image] PRIMARY KEY CLUSTERED 
(
	[error_report_image_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [report_system].[error_report_image]  WITH CHECK ADD  CONSTRAINT [FK_error_report_image_error_report] FOREIGN KEY([error_report_id])
REFERENCES [report_system].[error_report] ([error_report_id])
GO

ALTER TABLE [report_system].[error_report_image] CHECK CONSTRAINT [FK_error_report_image_error_report]
GO


/****** Object:  Table [security_system].[object]    Script Date: 19/09/2024 11:14:11 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [security_system].[object](
	[object_name] [nvarchar](250) NOT NULL,
 CONSTRAINT [PK_object] PRIMARY KEY CLUSTERED 
(
	[object_name] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [security_system].[object_type]    Script Date: 19/09/2024 11:14:25 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [security_system].[object_type](
	[object_type_name] [nvarchar](100) NOT NULL,
 CONSTRAINT [PK_object_type] PRIMARY KEY CLUSTERED 
(
	[object_type_name] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [security_system].[operation]    Script Date: 19/09/2024 11:14:33 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [security_system].[operation](
	[operation_name] [nvarchar](100) NOT NULL,
 CONSTRAINT [PK_operation] PRIMARY KEY CLUSTERED 
(
	[operation_name] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [security_system].[permission]    Script Date: 19/09/2024 11:14:48 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [security_system].[permission](
	[permission_id] [int] IDENTITY(1,1) NOT NULL,
	[permission_desc] [nvarchar](100) NOT NULL,
	[operation_name] [nvarchar](100) NOT NULL,
	[object_name] [nvarchar](250) NOT NULL,
	[object_type] [nvarchar](100) NOT NULL,
 CONSTRAINT [PK_permission] PRIMARY KEY CLUSTERED 
(
	[permission_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [NK_permission] UNIQUE NONCLUSTERED 
(
	[permission_desc] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [UN_operation] UNIQUE NONCLUSTERED 
(
	[permission_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [security_system].[permission]  WITH CHECK ADD  CONSTRAINT [FK_permission_object] FOREIGN KEY([object_name])
REFERENCES [security_system].[object] ([object_name])
ON UPDATE CASCADE
GO

ALTER TABLE [security_system].[permission] CHECK CONSTRAINT [FK_permission_object]
GO

ALTER TABLE [security_system].[permission]  WITH CHECK ADD  CONSTRAINT [FK_permission_object_type] FOREIGN KEY([object_type])
REFERENCES [security_system].[object_type] ([object_type_name])
ON UPDATE CASCADE
GO

ALTER TABLE [security_system].[permission] CHECK CONSTRAINT [FK_permission_object_type]
GO

ALTER TABLE [security_system].[permission]  WITH CHECK ADD  CONSTRAINT [FK_permission_operation] FOREIGN KEY([operation_name])
REFERENCES [security_system].[operation] ([operation_name])
ON UPDATE CASCADE
GO

ALTER TABLE [security_system].[permission] CHECK CONSTRAINT [FK_permission_operation]
GO

/****** Object:  Table [security_system].[role]    Script Date: 19/09/2024 11:15:25 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [security_system].[role](
	[role_id] [int] IDENTITY(10000,7) NOT NULL,
	[role_desc] [nvarchar](250) NOT NULL,
 CONSTRAINT [PK_role] PRIMARY KEY CLUSTERED 
(
	[role_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [NK_role] UNIQUE NONCLUSTERED 
(
	[role_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [security_system].[resource_role]    Script Date: 19/09/2024 11:15:11 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [security_system].[resource_role](
	[hr_id] [int] NOT NULL,
	[role_id] [int] NOT NULL,
 CONSTRAINT [PK_resource_role] PRIMARY KEY CLUSTERED 
(
	[hr_id] ASC,
	[role_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [security_system].[resource_role]  WITH CHECK ADD  CONSTRAINT [FK_resource_role_human_resource] FOREIGN KEY([hr_id])
REFERENCES [hr_system].[human_resource] ([hr_id])
GO

ALTER TABLE [security_system].[resource_role] CHECK CONSTRAINT [FK_resource_role_human_resource]
GO

ALTER TABLE [security_system].[resource_role]  WITH CHECK ADD  CONSTRAINT [FK_resource_role_role] FOREIGN KEY([role_id])
REFERENCES [security_system].[role] ([role_id])
GO

ALTER TABLE [security_system].[resource_role] CHECK CONSTRAINT [FK_resource_role_role]
GO

/****** Object:  Table [security_system].[role_permission]    Script Date: 19/09/2024 11:15:48 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [security_system].[role_permission](
	[role_id] [int] NOT NULL,
	[permission_id] [int] NOT NULL,
 CONSTRAINT [PK_role_permission] PRIMARY KEY CLUSTERED 
(
	[role_id] ASC,
	[permission_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [security_system].[role_permission]  WITH CHECK ADD  CONSTRAINT [FK_role_permission_permission] FOREIGN KEY([permission_id])
REFERENCES [security_system].[permission] ([permission_id])
GO

ALTER TABLE [security_system].[role_permission] CHECK CONSTRAINT [FK_role_permission_permission]
GO

ALTER TABLE [security_system].[role_permission]  WITH CHECK ADD  CONSTRAINT [FK_role_permission_role] FOREIGN KEY([role_id])
REFERENCES [security_system].[role] ([role_id])
GO

ALTER TABLE [security_system].[role_permission] CHECK CONSTRAINT [FK_role_permission_role]
GO

INSERT INTO quoting_system_db.branch (
	branch_name
)
VALUES
	('Deer Park'),
	('North Pole');

INSERT INTO quoting_system_db.contact (
	contact_first_name,
	contact_last_name,
	contact_pref_name
)
VALUES 
	('Joanne', 'Bambi', 'Bam'),
	('John', 'Doe', NULL),
	('Jane', 'Buck', NULL),
	('Jamie', 'Deer', NULL),
	('Jack', 'Stag', 'Whisk'),
	('Deerdre', 'Smith', NULL);

INSERT INTO hr_system.resource_group_category (
	group_category_name
)
VALUES
	('Uncategorised');
	
INSERT INTO hr_system.resource_group (
	group_name,
	group_parent_group,
	group_category_name
)
VALUES
	('Assembly', NULL, 'Uncategorised'),
	('CNC', NULL, 'Uncategorised'),
	('Machine Shop', NULL, 'Uncategorised'),
	('Dispatch', NULL, 'Uncategorised'),
	('Geometric', NULL, 'Uncategorised');
	
INSERT INTO hr_system.human_resource (
	hr_job_title,
	contact_id,
	hr_supervisor_id,
	branch_name,
	hr_pin
)
VALUES
	('Labourer', 
	 (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Joanne' AND contact_last_name = 'Bambi'),
	 NULL,
	 'Deer Park',
	 '1234'),
	('Labourer', 
	 (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'John' AND contact_last_name = 'Doe'),
	 NULL,
	 'Deer Park',
	 '2345'),
	('Tradesperson', 
	 (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Jane' AND contact_last_name = 'Buck'),
	 NULL,
	 'Deer Park',
	 '3456'),
	('Carpenter''s Assistant', 
	 (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Jack' AND contact_last_name = 'Stag'),
	 NULL,
	 'Deer Park',
	 '3456'),
	('Tradesperson', 
	 (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Deerdre' AND contact_last_name = 'Smith'),
	 NULL,
	 'Deer Park',
	 '4567');
	 
INSERT INTO integrations.asana_operations_project (
	project_gid,
	is_worklist,
	worklist_complete,
	worklist_yes,
	worklist_no,
	worklist_in_progress
)
VALUES
	('1108959633630000', 1, '1108959633630000', '1108959633630001', '1108959633630002', '1108959633630003'),
	('1208959633630001', 1, '1208959633630000', '1208959633630001', '1208959633630002', '1208959633630003'),
	('1308959633630002', 1, '1308959633630000', '1308959633630001', '1308959633630002', '1308959633630003'),
	('1408959633630003', 1, '1408959633630000', '1408959633630001', '1408959633630002', '1408959633630003'),
	('1508959633630004', 1, '1508959633630000', '1508959633630001', '1508959633630002', '1508959633630003');
	
INSERT INTO integrations.asana_project_resource_group (
	resource_group_id,
	asana_projecT_gid
)
VALUES
	((SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Assembly'), '1108959633630000'),
	((SELECT group_id FROM hr_system.resource_group WHERE group_name = 'CNC'), '1208959633630001'),
	((SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Machine Shop'), '1308959633630002'),
	((SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Dispatch'), '1408959633630003'),
	((SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Geometric'), '1508959633630004');
	
INSERT INTO integrations.asana_task (
	task_name,
	task_gid,
	stair_category
)
VALUES
	('100000 #123 Canada Close DEER PARK (MOOSE CONSTRUCTIONS)', '1230000000000123', 'T-1'),
	('100001 #2 Bullwinkle Blvd BRAESIDE (FALLOW HOMES)', '2540000000000123', 'T-2'),
	('100002 Lot 5 Elliot Ave RICHMOND (RED HOMES)', '6950000000000123', 'T-9'),
	('100003 Lot 6 #8 Rudolph Rd DEER PARK (FALLOW HOMES)', '4750000000000123', 'T-2'),
	('100004 6/21 Donner Drv MELTON (WHITE STAG)', '1238500000000123', 'T-5');
	
INSERT INTO production_system.job_tracking_entry (
	entry_date,
	entry_branch_name,
	entry_area_group_id,
	entry_hr_id,
	entry_task_gid,
	entry_start_time,
	entry_end_time,
	entry_comment
)
VALUES
	('2024-09-01', 
	 'Deer Park', 
	 (SELECT group_id FROM hr_system.resource_group WHERE group_name = 'CNC'),			
	 (SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Joanne' AND contact_last_name = 'Bambi')), 
	 '1230000000000123', 
	 '2024-09-01 10:00:00', 
	 '2024-09-01 11:31:00',
	 NULL),
	('2024-09-01', 
	 'Deer Park', 
	 (SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Assembly'),		
	 (SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'John' AND contact_last_name = 'Doe')), 
	 '2540000000000123', 
	 '2024-09-01 11:54:00', 
	 '2024-09-01 14:02:00',
	 'Have you noticed all the deer jokes?'),
	('2024-09-02', 
	 'Deer Park', 
	 (SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Assembly'),		
	 (SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'John' AND contact_last_name = 'Doe')), 
	 '1230000000000123', 
	 '2024-09-02 09:30:00', 
	 '2024-09-02 11:42:00',
	 'Can''t think of another deer pun'),
	('2024-09-02', 
	 'Deer Park', 
	 (SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Machine Shop'),	
	 (SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Deerdre' AND contact_last_name = 'Smith')), 
	 '4750000000000123', 
	 '2024-09-02 13:01:00', 
	 '2024-09-02 14:15:00',
	 'What do you call a deer with no eyes? No idea.'),
	('2024-09-03', 
	 'Deer Park', 
	 (SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Dispatch'),		
	 (SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Jane' AND contact_last_name = 'Buck')), 
	 '1230000000000123', 
	 '2024-09-03 07:26:00', 
	 '2024-09-03 10:01:00',
	 NULL);
	 
INSERT INTO production_system.job_tracking_entry_image (
	entry_id,
	entry_image_url
)
VALUES
	((SELECT TOP(1) entry_id FROM production_system.job_tracking_entry),
	 'https://upload.wikimedia.org/wikipedia/commons/a/a7/A_chital_stag_1.JPG'),
	((SELECT entry_id FROM production_system.job_tracking_entry ORDER BY entry_date OFFSET 1 ROWS FETCH NEXT 1 ROW ONLY), 
	 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQymPDHGtmSbJisYr97FFOOvNwUGqiYR2ssgw&s'),
	((SELECT entry_id FROM production_system.job_tracking_entry ORDER BY entry_date OFFSET 2 ROWS FETCH NEXT 1 ROW ONLY), 
	 'https://www.reddit.com/media?url=https%3A%2F%2Fpreview.redd.it%2Fthese-funny-deer-checking-the-camera-out-v0-tafx9vru32sc1.jpeg%3Fwidth%3D640%26crop%3Dsmart%26auto%3Dwebp%26s%3D9a82f38db804630f71ebcd7a1965324b394fc4ac'),
	((SELECT entry_id FROM production_system.job_tracking_entry ORDER BY entry_date OFFSET 3 ROWS FETCH NEXT 1 ROW ONLY), 
	 'https://nypost.com/wp-content/uploads/sites/2/2015/06/tiny_baby_deer.jpg?quality=75&strip=all&w=740'),
	((SELECT entry_id FROM production_system.job_tracking_entry ORDER BY entry_date OFFSET 4 ROWS FETCH NEXT 1 ROW ONLY), 
	 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRscA3f2jHwYKJKUgW8UrN2w8A_PG5M23fBPQ&s');
	 
INSERT INTO quality_system.error (
	error_desc,
	error_department
)
VALUES
	('Stair type incorrect on order',		(SELECT group_id FROM hr_system.resource_group WHERE group_name = 'CNC')),
	('Tread size incorrect on order',		(SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Assembly')),
	('Stringer size incorrect on order',	(SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Machine Shop')),
	('Stringer type incorrect on order',	(SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Dispatch')),
	('Number of rises incorrect on order',	(SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Assembly'));
	
INSERT INTO quality_system.error_group (
	error_group_name
)
VALUES
	('Order Error'),
	('Stringer Error'),
	('Size Error'),
	('Plans Error'),
	('Template Error');
	
INSERT INTO quality_system.error_group_error (
	error_id,
	error_group_id
)
VALUES
	((SELECT error_id FROM quality_system.error WHERE error_desc = 'Stringer size incorrect on order'),
	 (SELECT error_group_id FROM quality_system.error_group WHERE error_group_name = 'Order Error')),
	((SELECT error_id FROM quality_system.error WHERE error_desc = 'Stringer size incorrect on order'),
	 (SELECT error_group_id FROM quality_system.error_group WHERE error_group_name = 'Stringer Error')),
	((SELECT error_id FROM quality_system.error WHERE error_desc = 'Stringer size incorrect on order'),
	 (SELECT error_group_id FROM quality_system.error_group WHERE error_group_name = 'Size Error'));
	 
INSERT INTO report_system.error_report (
	reported_at_department,
	hr_id,
	task_gid,
	reported_at_time,
	comments
)
VALUES
	((SELECT group_id FROM hr_system.resource_group WHERE group_name = 'CNC'),
	 (SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id 
																	 FROM quoting_system_db.contact 
																	 WHERE contact_first_name = 'Joanne' 
																		AND contact_last_name = 'Bambi')),
	 '2540000000000123',
	 DATEADD(DAY, -2, getdate()),
	 'Too many deer'),
	((SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Assembly'),
	 (SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id 
																	 FROM quoting_system_db.contact 
																	 WHERE contact_first_name = 'John' 
																		AND contact_last_name = 'Doe')),
	 '2540000000000123',
	 DATEADD(DAY, -1, getdate()),
	 'Not enough deer'),
	((SELECT group_id FROM hr_system.resource_group WHERE group_name = 'Machine Shop'),
	 (SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id 
																	 FROM quoting_system_db.contact 
																	 WHERE contact_first_name = 'Jane' 
																		AND contact_last_name = 'Buck')),
	 '1230000000000123',
	 getdate(),
	 'This deer has buck teeth');
	 
INSERT INTO report_system.error_report_error (
	error_report_id,
	error_id
)
VALUES
	((SELECT error_report_id FROM report_system.error_report WHERE comments = 'Too many deer'),
	 (SELECT error_id FROM quality_system.error WHERE error_desc = 'Stringer size incorrect on order')),
	((SELECT error_report_id FROM report_system.error_report WHERE comments = 'Too many deer'),
	 (SELECT error_id FROM quality_system.error WHERE error_desc = 'Tread size incorrect on order')),
	((SELECT error_report_id FROM report_system.error_report WHERE comments = 'Not enough deer'),
	 (SELECT error_id FROM quality_system.error WHERE error_desc = 'Stringer type incorrect on order')),
	((SELECT error_report_id FROM report_system.error_report WHERE comments = 'This deer has buck teeth'),
	 (SELECT error_id FROM quality_system.error WHERE error_desc = 'Number of rises incorrect on order'));
	 
INSERT INTO report_system.error_report_image (
	error_report_id,
	image_url
)
VALUES
	((SELECT error_report_id FROM report_system.error_report WHERE comments = 'Too many deer'),
	 'https://live.staticflickr.com/3627/3675613957_49559fcfd1_b.jpg'),
	((SELECT error_report_id FROM report_system.error_report WHERE comments = 'Not enough deer'),
	 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvBosKFVnWL2gAz3CwxfQ7_EywSZBxNHUdxg&s'),
	((SELECT error_report_id FROM report_system.error_report WHERE comments = 'This deer has buck teeth'),
	 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdJ7_opNZwaIwHynP0Z43lG2cZ5BKOtSl0Ew&s');
	
INSERT INTO security_system.object (
	object_name
)
VALUES
	('Department Details'),
	('Detailing Spec Sheet'),
	('Human Resource Group'),
	('Job Details'),
	('Time Tracking App'),
	('Job Tracking Entry');

INSERT INTO security_system.object_type (
	object_type_name
)
VALUES
	('Database Table'),
	('Web Application'),
	('Web Application Page');

INSERT INTO security_system.operation (
	operation_name
)
VALUES
	('Create'),
	('Delete'),
	('Read'),
	('Update');

INSERT INTO security_system.permission (
	permission_desc,
	operation_name,
	object_name,
	object_type
)
VALUES
	('Create Human Resource Group',		'Create', 'Human Resource Group', 'Database Table'),
	('Read Human Resource Group',		'Read', 'Human Resource Group', 'Database Table'),
	('Update Human Resource Group',		'Update', 'Human Resource Group', 'Database Table'),
	('Delete Human Resource Group',		'Delete', 'Human Resource Group', 'Database Table'),
	('Create Job Tracking Entry',		'Create', 'Job Tracking Entry', 'Database Table'),
	('Read Job Tracking Entry',			'Read', 'Job Tracking Entry', 'Database Table'),
	('Update Job Tracking Entry',		'Update', 'Job Tracking Entry', 'Database Table'),
	('Create Job Details',				'Create', 'Job Details', 'Web Application Page'),
	('Read Job Details',				'Read', 'Job Details', 'Web Application Page'),
	('Update Job Details',				'Update', 'Job Details', 'Web Application Page'),
	('Delete Job Details',				'Delete', 'Job Details', 'Web Application Page'),
	('Create Time Tracking App',		'Create', 'Time Tracking App', 'Web Application'),
	('Read Time Tracking App',			'Read', 'Time Tracking App', 'Web Application'),
	('Update Time Tracking App',		'Update', 'Time Tracking App', 'Web Application'),
	('Delete Time Tracking App',		'Delete', 'Time Tracking App', 'Web Application'),
	('Create Department Details',		'Create', 'Department Details', 'Web Application Page'),
	('Read Department Details',			'Read', 'Department Details', 'Web Application Page'),
	('Update Department Details',		'Update', 'Department Details', 'Web Application Page'),
	('Delete Department Details',		'Delete', 'Department Details', 'Web Application Page'),
	('Read Detailing Spec Sheet',		'Read', 'Detailing Spec Sheet', 'Web Application'),
	('Create Detailing Spec Sheet',		'Create', 'Detailing Spec Sheet', 'Web Application');
	
INSERT INTO security_system.role (
	role_desc
)
VALUES
	('Systems Administrator'),
	('Time Tracking Application'),
	('HQ User'),
	('Kiosk Admin'),
	('Detailer');
	
INSERT INTO security_system.resource_role (
	hr_id,
	role_id
)
VALUES
	((SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Joanne' AND contact_last_name = 'Bambi')),
	 (SELECT role_id FROM security_system.role WHERE role_desc = 'Kiosk Admin')),
	((SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'John' AND contact_last_name = 'Doe')),
	 (SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application')),
	((SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Joanne' AND contact_last_name = 'Bambi')),
	 (SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application')),
	((SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Jane' AND contact_last_name = 'Buck')),
	 (SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application')),
	((SELECT hr_id FROM hr_system.human_resource WHERE contact_id = (SELECT contact_id FROM quoting_system_db.contact WHERE contact_first_name = 'Deerdre' AND contact_last_name = 'Smith')),
	 (SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'))
	 
INSERT INTO security_system.role_permission (
	role_id,
	permission_id
)
VALUES
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Create Department Details')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Read Department Details')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Update Department Details')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Delete Department Details')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Read Job Details')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Update Job Details')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Create Time Tracking App')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Read Time Tracking App')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Update Time Tracking App')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Time Tracking Application'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Delete Time Tracking App')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'HQ User'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Create Time Tracking App')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Kiosk Admin'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Update Human Resource Group')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Kiosk Admin'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Create Department Details')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Kiosk Admin'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Read Department Details')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Detailer'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Read Detailing Spec Sheet')),
	((SELECT role_id FROM security_system.role WHERE role_desc = 'Detailer'),
	 (SELECT permission_id FROM security_system.permission WHERE permission_desc = 'Create Detailing Spec Sheet'));


