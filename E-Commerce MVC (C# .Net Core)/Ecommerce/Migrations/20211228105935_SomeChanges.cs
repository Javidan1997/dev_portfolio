using Microsoft.EntityFrameworkCore.Migrations;

namespace Parviz_Web_app.Migrations
{
    public partial class SomeChanges : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_ActivityofMonths_Categories_CategoryId",
                table: "ActivityofMonths");

            migrationBuilder.DropPrimaryKey(
                name: "PK_ActivityofMonths",
                table: "ActivityofMonths");

            migrationBuilder.RenameTable(
                name: "ActivityofMonths",
                newName: "Activityofmonths");

            migrationBuilder.RenameIndex(
                name: "IX_ActivityofMonths_CategoryId",
                table: "Activityofmonths",
                newName: "IX_Activityofmonths_CategoryId");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Activityofmonths",
                table: "Activityofmonths",
                column: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_Activityofmonths_Categories_CategoryId",
                table: "Activityofmonths",
                column: "CategoryId",
                principalTable: "Categories",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Activityofmonths_Categories_CategoryId",
                table: "Activityofmonths");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Activityofmonths",
                table: "Activityofmonths");

            migrationBuilder.RenameTable(
                name: "Activityofmonths",
                newName: "ActivityofMonths");

            migrationBuilder.RenameIndex(
                name: "IX_Activityofmonths_CategoryId",
                table: "ActivityofMonths",
                newName: "IX_ActivityofMonths_CategoryId");

            migrationBuilder.AddPrimaryKey(
                name: "PK_ActivityofMonths",
                table: "ActivityofMonths",
                column: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_ActivityofMonths_Categories_CategoryId",
                table: "ActivityofMonths",
                column: "CategoryId",
                principalTable: "Categories",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
