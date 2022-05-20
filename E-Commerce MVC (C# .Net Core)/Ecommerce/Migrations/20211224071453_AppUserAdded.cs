using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace Parviz_Web_app.Migrations
{
    public partial class AppUserAdded : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_ActivityofMonths_ActivityofMonths_ActivityOfMonthId",
                table: "ActivityofMonths");

            migrationBuilder.DropIndex(
                name: "IX_ActivityofMonths_ActivityOfMonthId",
                table: "ActivityofMonths");

            migrationBuilder.DropColumn(
                name: "ActivityOfMonthId",
                table: "ActivityofMonths");

            migrationBuilder.CreateTable(
                name: "AppUsers",
                columns: table => new
                {
                    Id = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    FullName = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    IsMember = table.Column<bool>(type: "bit", nullable: false),
                    IsActive = table.Column<bool>(type: "bit", nullable: false),
                    UserName = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    NormalizedUserName = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    Email = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    NormalizedEmail = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    EmailConfirmed = table.Column<bool>(type: "bit", nullable: false),
                    PasswordHash = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    SecurityStamp = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    ConcurrencyStamp = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    PhoneNumber = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    PhoneNumberConfirmed = table.Column<bool>(type: "bit", nullable: false),
                    TwoFactorEnabled = table.Column<bool>(type: "bit", nullable: false),
                    LockoutEnd = table.Column<DateTimeOffset>(type: "datetimeoffset", nullable: true),
                    LockoutEnabled = table.Column<bool>(type: "bit", nullable: false),
                    AccessFailedCount = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AppUsers", x => x.Id);
                });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "AppUsers");

            migrationBuilder.AddColumn<int>(
                name: "ActivityOfMonthId",
                table: "ActivityofMonths",
                type: "int",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_ActivityofMonths_ActivityOfMonthId",
                table: "ActivityofMonths",
                column: "ActivityOfMonthId");

            migrationBuilder.AddForeignKey(
                name: "FK_ActivityofMonths_ActivityofMonths_ActivityOfMonthId",
                table: "ActivityofMonths",
                column: "ActivityOfMonthId",
                principalTable: "ActivityofMonths",
                principalColumn: "Id",
                onDelete: ReferentialAction.Restrict);
        }
    }
}
