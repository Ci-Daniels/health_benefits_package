

# Imporitng packages ------------------------------------------------------

pacman::p_load(
  shiny,
  shinydashboard,
  shiny,
  DBI,
  DT
)

# Creating the connection -------------------------------------------------


conn <-  dbConnect(
  RPostgres::Postgres(),
  dbname = "shif_health_essential_benefits_package",
  host = "localhost",
  port = 5432,
  user = "postgres",
  password = "c3mA_hUb"
)


