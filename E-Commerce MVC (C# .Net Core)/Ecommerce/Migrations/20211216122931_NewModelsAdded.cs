using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace Parviz_Web_app.Migrations
{
    public partial class NewModelsAdded : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "ActivityofMonths",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    CategoryId = table.Column<int>(type: "int", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(150)", maxLength: 150, nullable: true),
                    Desc = table.Column<string>(type: "nvarchar(1500)", maxLength: 1500, nullable: true),
                    CodePref = table.Column<string>(type: "nvarchar(10)", maxLength: 10, nullable: true),
                    CodeNum = table.Column<int>(type: "int", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false),
                    ActivityOfMonthId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ActivityofMonths", x => x.Id);
                    table.ForeignKey(
                        name: "FK_ActivityofMonths_ActivityofMonths_ActivityOfMonthId",
                        column: x => x.ActivityOfMonthId,
                        principalTable: "ActivityofMonths",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_ActivityofMonths_Categories_CategoryId",
                        column: x => x.CategoryId,
                        principalTable: "Categories",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "Recentworks",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    CategoryId = table.Column<int>(type: "int", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(150)", maxLength: 150, nullable: true),
                    Desc = table.Column<string>(type: "nvarchar(1500)", maxLength: 1500, nullable: true),
                    CodePref = table.Column<string>(type: "nvarchar(10)", maxLength: 10, nullable: true),
                    CodeNum = table.Column<int>(type: "int", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Recentworks", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Recentworks_Categories_CategoryId",
                        column: x => x.CategoryId,
                        principalTable: "Categories",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "ActivityofMonthPhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    ActivityofMonthId = table.Column<int>(type: "int", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ActivityofMonthPhotos", x => x.Id);
                    table.ForeignKey(
                        name: "FK_ActivityofMonthPhotos_ActivityofMonths_ActivityofMonthId",
                        column: x => x.ActivityofMonthId,
                        principalTable: "ActivityofMonths",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "RecentworkPhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    RecentworkId = table.Column<int>(type: "int", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_RecentworkPhotos", x => x.Id);
                    table.ForeignKey(
                        name: "FK_RecentworkPhotos_Recentworks_RecentworkId",
                        column: x => x.RecentworkId,
                        principalTable: "Recentworks",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_ActivityofMonthPhotos_ActivityofMonthId",
                table: "ActivityofMonthPhotos",
                column: "ActivityofMonthId");

            migrationBuilder.CreateIndex(
                name: "IX_ActivityofMonths_ActivityOfMonthId",
                table: "ActivityofMonths",
                column: "ActivityOfMonthId");

            migrationBuilder.CreateIndex(
                name: "IX_ActivityofMonths_CategoryId",
                table: "ActivityofMonths",
                column: "CategoryId");

            migrationBuilder.CreateIndex(
                name: "IX_RecentworkPhotos_RecentworkId",
                table: "RecentworkPhotos",
                column: "RecentworkId");

            migrationBuilder.CreateIndex(
                name: "IX_Recentworks_CategoryId",
                table: "Recentworks",
                column: "CategoryId");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "ActivityofMonthPhotos");

            migrationBuilder.DropTable(
                name: "RecentworkPhotos");

            migrationBuilder.DropTable(
                name: "ActivityofMonths");

            migrationBuilder.DropTable(
                name: "Recentworks");
        }
    }
}
