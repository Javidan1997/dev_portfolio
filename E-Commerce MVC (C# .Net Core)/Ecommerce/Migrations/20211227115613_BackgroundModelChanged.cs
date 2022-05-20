using Microsoft.EntityFrameworkCore.Migrations;

namespace Parviz_Web_app.Migrations
{
    public partial class BackgroundModelChanged : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "BackgroundPhotos");

            migrationBuilder.AddColumn<string>(
                name: "Photo",
                table: "Backgrounds",
                type: "nvarchar(max)",
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Photo",
                table: "Backgrounds");

            migrationBuilder.CreateTable(
                name: "BackgroundPhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    BackgroundId = table.Column<int>(type: "int", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_BackgroundPhotos", x => x.Id);
                    table.ForeignKey(
                        name: "FK_BackgroundPhotos_Backgrounds_BackgroundId",
                        column: x => x.BackgroundId,
                        principalTable: "Backgrounds",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_BackgroundPhotos_BackgroundId",
                table: "BackgroundPhotos",
                column: "BackgroundId");
        }
    }
}
