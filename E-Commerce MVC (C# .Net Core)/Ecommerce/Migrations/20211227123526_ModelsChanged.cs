using Microsoft.EntityFrameworkCore.Migrations;

namespace Parviz_Web_app.Migrations
{
    public partial class ModelsChanged : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "AboutPhotos");

            migrationBuilder.DropTable(
                name: "ActivityofMonthPhotos");

            migrationBuilder.DropTable(
                name: "InstagramPhotos");

            migrationBuilder.DropTable(
                name: "PeoplePhotos");

            migrationBuilder.DropTable(
                name: "RecentworkPhotos");

            migrationBuilder.DropTable(
                name: "TattooPhotos");

            migrationBuilder.DropTable(
                name: "TwitterPhotos");

            migrationBuilder.AddColumn<string>(
                name: "Photo",
                table: "Twitters",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Photo",
                table: "Tattoos",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Photo",
                table: "Recentworks",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Photo",
                table: "Peoples",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Photo",
                table: "Instagrams",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Photo",
                table: "ActivityofMonths",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "Photo",
                table: "Abouts",
                type: "nvarchar(max)",
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Photo",
                table: "Twitters");

            migrationBuilder.DropColumn(
                name: "Photo",
                table: "Tattoos");

            migrationBuilder.DropColumn(
                name: "Photo",
                table: "Recentworks");

            migrationBuilder.DropColumn(
                name: "Photo",
                table: "Peoples");

            migrationBuilder.DropColumn(
                name: "Photo",
                table: "Instagrams");

            migrationBuilder.DropColumn(
                name: "Photo",
                table: "ActivityofMonths");

            migrationBuilder.DropColumn(
                name: "Photo",
                table: "Abouts");

            migrationBuilder.CreateTable(
                name: "AboutPhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    AboutId = table.Column<int>(type: "int", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AboutPhotos", x => x.Id);
                    table.ForeignKey(
                        name: "FK_AboutPhotos_Abouts_AboutId",
                        column: x => x.AboutId,
                        principalTable: "Abouts",
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
                name: "InstagramPhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    InstagramId = table.Column<int>(type: "int", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_InstagramPhotos", x => x.Id);
                    table.ForeignKey(
                        name: "FK_InstagramPhotos_Instagrams_InstagramId",
                        column: x => x.InstagramId,
                        principalTable: "Instagrams",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "PeoplePhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PeopleId = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_PeoplePhotos", x => x.Id);
                    table.ForeignKey(
                        name: "FK_PeoplePhotos_Peoples_PeopleId",
                        column: x => x.PeopleId,
                        principalTable: "Peoples",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "RecentworkPhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true),
                    RecentworkId = table.Column<int>(type: "int", nullable: false)
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

            migrationBuilder.CreateTable(
                name: "TattooPhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true),
                    TattooId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_TattooPhotos", x => x.Id);
                    table.ForeignKey(
                        name: "FK_TattooPhotos_Tattoos_TattooId",
                        column: x => x.TattooId,
                        principalTable: "Tattoos",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "TwitterPhotos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Order = table.Column<int>(type: "int", nullable: false),
                    PosterStatus = table.Column<bool>(type: "bit", nullable: true),
                    TwitterId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_TwitterPhotos", x => x.Id);
                    table.ForeignKey(
                        name: "FK_TwitterPhotos_Twitters_TwitterId",
                        column: x => x.TwitterId,
                        principalTable: "Twitters",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_AboutPhotos_AboutId",
                table: "AboutPhotos",
                column: "AboutId");

            migrationBuilder.CreateIndex(
                name: "IX_ActivityofMonthPhotos_ActivityofMonthId",
                table: "ActivityofMonthPhotos",
                column: "ActivityofMonthId");

            migrationBuilder.CreateIndex(
                name: "IX_InstagramPhotos_InstagramId",
                table: "InstagramPhotos",
                column: "InstagramId");

            migrationBuilder.CreateIndex(
                name: "IX_PeoplePhotos_PeopleId",
                table: "PeoplePhotos",
                column: "PeopleId");

            migrationBuilder.CreateIndex(
                name: "IX_RecentworkPhotos_RecentworkId",
                table: "RecentworkPhotos",
                column: "RecentworkId");

            migrationBuilder.CreateIndex(
                name: "IX_TattooPhotos_TattooId",
                table: "TattooPhotos",
                column: "TattooId");

            migrationBuilder.CreateIndex(
                name: "IX_TwitterPhotos_TwitterId",
                table: "TwitterPhotos",
                column: "TwitterId");
        }
    }
}
