using Microsoft.EntityFrameworkCore.Migrations;

namespace Parviz_Web_app.Migrations
{
    public partial class SocialMediaChanged : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Link",
                table: "SocialMedias");

            migrationBuilder.DropColumn(
                name: "Name",
                table: "SocialMedias");

            migrationBuilder.AddColumn<string>(
                name: "FacebookLink",
                table: "SocialMedias",
                type: "nvarchar(800)",
                maxLength: 800,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "GooglePlusLink",
                table: "SocialMedias",
                type: "nvarchar(800)",
                maxLength: 800,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "PinterestLink",
                table: "SocialMedias",
                type: "nvarchar(800)",
                maxLength: 800,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "TwitterLink",
                table: "SocialMedias",
                type: "nvarchar(800)",
                maxLength: 800,
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "FacebookLink",
                table: "SocialMedias");

            migrationBuilder.DropColumn(
                name: "GooglePlusLink",
                table: "SocialMedias");

            migrationBuilder.DropColumn(
                name: "PinterestLink",
                table: "SocialMedias");

            migrationBuilder.DropColumn(
                name: "TwitterLink",
                table: "SocialMedias");

            migrationBuilder.AddColumn<string>(
                name: "Link",
                table: "SocialMedias",
                type: "nvarchar(600)",
                maxLength: 600,
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<string>(
                name: "Name",
                table: "SocialMedias",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: false,
                defaultValue: "");
        }
    }
}
