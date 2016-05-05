
CREATE TABLE [dbo].[DOTAAC_Feeds](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[PageId] [bigint] NULL,
	[FeedId] [varchar](100) NOT NULL,
	[FeedMessage] [varchar](3000) NULL,
	[LinkName] [varchar](200) NULL,
	[FeedType] [char](10) NULL,
	[FeedLink] [varchar](300) NULL,
	[PublishedDate] [datetime] NOT NULL,
	[LikesCount] [int] NOT NULL,
	[CommentsCount] [int] NOT NULL,
	[SharesCount] [int] NOT NULL,
	[FeedStatus] [tinyint] NOT NULL,
 CONSTRAINT [PK_DOTAAC_Feeds] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


ALTER TABLE [dbo].[DOTAAC_Feeds] ADD  DEFAULT ((1)) FOR [FeedStatus]
GO


