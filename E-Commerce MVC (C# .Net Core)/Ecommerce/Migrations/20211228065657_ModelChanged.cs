using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace Parviz_Web_app.Migrations
{
    public partial class ModelChanged : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "CodeNum",
                table: "Tattoos");

            migrationBuilder.DropColumn(
                name: "CodePref",
                table: "Tattoos");

            migrationBuilder.DropColumn(
                name: "CreatedAt",
                table: "Tattoos");

            migrationBuilder.DropColumn(
                name: "CodeNum",
                table: "Recentworks");

            migrationBuilder.DropColumn(
                name: "CodePref",
                table: "Recentworks");

            migrationBuilder.DropColumn(
                name: "CreatedAt",
                table: "Recentworks");

            migrationBuilder.DropColumn(
                name: "CodeNum",
                table: "ActivityofMonths");

            migrationBuilder.DropColumn(
                name: "CodePref",
                table: "ActivityofMonths");

            migrationBuilder.DropColumn(
                name: "CreatedAt",
                table: "ActivityofMonths");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "CodeNum",
                table: "Tattoos",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<string>(
                name: "CodePref",
                table: "Tattoos",
                type: "nvarchar(10)",
                maxLength: 10,
                nullable: true);

            migrationBuilder.AddColumn<DateTime>(
                name: "CreatedAt",
                table: "Tattoos",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<int>(
                name: "CodeNum",
                table: "Recentworks",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<string>(
                name: "CodePref",
                table: "Recentworks",
                type: "nvarchar(10)",
                maxLength: 10,
                nullable: true);

            migrationBuilder.AddColumn<DateTime>(
                name: "CreatedAt",
                table: "Recentworks",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<int>(
                name: "CodeNum",
                table: "ActivityofMonths",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<string>(
                name: "CodePref",
                table: "ActivityofMonths",
                type: "nvarchar(10)",
                maxLength: 10,
                nullable: true);

            migrationBuilder.AddColumn<DateTime>(
                name: "CreatedAt",
                table: "ActivityofMonths",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));
        }
    }
}
