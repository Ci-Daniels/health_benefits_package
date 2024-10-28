# Load the required libraries
source('global.R')

# Define the UI 
ui <- dashboardPage(
  dashboardHeader(title = "Health Essential Benefits Package Dashboard"),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Home", tabName = "home", icon = icon("home"), selected = TRUE),
      menuItem("Health Packages", icon = icon("list"),
               menuSubItem("Conditions Data", tabName = "conditions"),
               menuSubItem("Medicine Data", tabName = "medicine"),
               menuSubItem("Manufacturers Data", tabName = "manufacturer"),
               menuSubItem("SHIF Fund", tabName = "shif"),
               menuSubItem("PHC Fund", tabName = "phc"),
               menuSubItem("Emergency Fund", tabName = "emergency"),
               menuSubItem("Chronic Fund", tabName = "chronic")
      )
    )
  ),
  
  dashboardBody(
    tags$head(
      tags$style(HTML("
    .dt-button {
      margin: 5px;  
      font-size: 24px;  
    }
    .dt-buttons {
      text-align: center;  
      margin-bottom: 20px;  
    }
      "))
    ),
    
    
    tabItems(
      tabItem(tabName = "home",
              h2("Welcome to the Essential Benefits Package Dashboard"),
              p("The dashboard allows you to explore the different essential medical packages. Use the navigation bar to select a table and view its contents."),
              tags$img(src = "https://media.istockphoto.com/id/1480239160/photo/an-analyst-uses-a-computer-and-dashboard-for-data-business-analysis-and-data-management.jpg?s=612x612&w=0&k=20&c=Zng3q0-BD8rEl0r6ZYZY0fbt2AWO9q_gC8lSrwCIgdk=", height="auto", width = "100%")
      ), 

# conditions tab ----------------------------------------------------------
      tabItem(
        tabName = "conditions",
        fluidRow(
          column(
            12,
            dataTableOutput("conditions_table", width = "100%")
          )
        )),

# medicine tab ------------------------------------------------------------
      tabItem(
        tabName = "medicine",
        fluidRow(
          column(
            12,
            dataTableOutput("medicine_table", width = "100%")
          )
        )),

# manufacturers tab -------------------------------------------------------
      tabItem(
        tabName = "manufacturer",
        fluidRow(
          column(
            6,
            dataTableOutput("manufacturer_table", width = "100%")
          )
        )),

# shif fund tab -----------------------------------------------------------
      tabItem(
        tabName = "shif",
        fluidRow(
          column(
            6,
            dataTableOutput("shif_table", width = "100%")
          )
        )),

# phc fund tab ------------------------------------------------------------
      tabItem(
        tabName = "phc",
        fluidRow(
          column(
            6,
            dataTableOutput("phc_table", width = "100%")
          )
        )),

# emergency fund tab ------------------------------------------------------
      tabItem(
        tabName = "emergency",
        fluidRow(
          column(
            6,
            dataTableOutput("emergency_table", width = "100%")
          )
        )),

# chronic fund tab -------------------------------------------------------
      tabItem(
        tabName = "chronic",
        fluidRow(
          column(
            6,
            dataTableOutput("chronic_table", width = "100%")
          )
        )),
      )
    )
  )

# Define server logic
server <- function(input, output, session) {

# Render  conditions data -------------------------------------------------
  observeEvent(input$sidebarItemExpanded == "conditions", {
    
    # Fetch data from the "Conditions" table
    output$conditions_table <- renderDT({
      dbReadTable(conn, "Conditions") |>
        datatable(
          escape = FALSE,
          extensions = 'Buttons',
          rownames = FALSE,
          filter = 'top',
          options = list(
            searching = TRUE,
            paging = TRUE,
            bInfo = FALSE,
            scrollX = TRUE,
            autoWidth = TRUE,
            dom = 'tB',
            buttons = c('copy', 'csv', 'excel'),
            columnDefs = list(
              list(className = 'dt-center', targets = "_all")),
            pageLength = 20
          ),
          class = "cell-border hover"
        )
    })
    
  })

# Render medicine data ----------------------------------------------------
  observeEvent(input$sidebarItemExpanded == "medicine", {
    
    # Fetch data from the "Medicine " table
    output$medicine_table <- renderDT({
      dbReadTable(conn, "Medicine") |>
        datatable(
          escape = FALSE,
          extensions = 'Buttons',
          rownames = FALSE,
          filter = 'top',
          options = list(
            searching = TRUE,
            paging = TRUE,
            bInfo = FALSE,
            scrollX = TRUE,
            autoWidth = TRUE,
            dom = 'tB',
            buttons = c('copy', 'csv', 'excel'),
            columnDefs = list(
              list(className = 'dt-center', targets = "_all")),
            pageLength = 20
          ),
          class = "cell-border hover"
        )
    })
    
  })
  
# Render manufacturer data ------------------------------------------------
  observeEvent(input$sidebarItemExpanded == "manufacturer", {
    
    # Fetch data from the "Manufacturer" table
    output$manufacturer_table <- renderDT({
      dbReadTable(conn, "Manufacturer") |>
        datatable(
          escape = FALSE,
          extensions = 'Buttons',
          rownames = FALSE,
          filter = 'top',
          options = list(
            searching = TRUE,
            paging = TRUE,
            bInfo = FALSE,
            scrollX = TRUE,
            autoWidth = TRUE,
            dom = 'tB',
            buttons = c('copy', 'csv', 'excel'),
            columnDefs = list(
              list(className = 'dt-center', targets = "_all")),
            pageLength = 20
          ),
          class = "cell-border hover"
        )
    })
    
  })


# Render SHIF data --------------------------------------------------------
  observeEvent(input$sidebarItemExpanded == "shif", {
    
    # Fetch data from the "Medicine " table
    output$medicine_table <- renderDT({
      dbReadTable(conn, "SHIF_Fund") |>
        datatable(
          escape = FALSE,
          extensions = 'Buttons',
          rownames = FALSE,
          filter = 'top',
          options = list(
            searching = TRUE,
            paging = TRUE,
            bInfo = FALSE,
            scrollX = TRUE,
            autoWidth = TRUE,
            dom = 'tB',
            buttons = c('copy', 'csv', 'excel'),
            columnDefs = list(
              list(className = 'dt-center', targets = "_all")),
            pageLength = 20
          ),
          class = "cell-border hover"
        )
    })
    
  })

# Render PHC Data ---------------------------------------------------------
  observeEvent(input$sidebarItemExpanded == "phc", {
    
    # Fetch data from the "Medicine " table
    output$medicine_table <- renderDT({
      dbReadTable(conn, "PHC_Fund") |>
        datatable(
          escape = FALSE,
          extensions = 'Buttons',
          rownames = FALSE,
          filter = 'top',
          options = list(
            searching = TRUE,
            paging = TRUE,
            bInfo = FALSE,
            scrollX = TRUE,
            autoWidth = TRUE,
            dom = 'tB',
            buttons = c('copy', 'csv', 'excel'),
            columnDefs = list(
              list(className = 'dt-center', targets = "_all")),
            pageLength = 20
          ),
          class = "cell-border hover"
        )
    })
    
  })
  

# Render Emergency Data ---------------------------------------------------
  observeEvent(input$sidebarItemExpanded == "emergency", {
    
    # Fetch data from the "Medicine " table
    output$medicine_table <- renderDT({
      dbReadTable(conn, "Emergency_Fund") |>
        datatable(
          escape = FALSE,
          extensions = 'Buttons',
          rownames = FALSE,
          filter = 'top',
          options = list(
            searching = TRUE,
            paging = TRUE,
            bInfo = FALSE,
            scrollX = TRUE,
            autoWidth = TRUE,
            dom = 'tB',
            buttons = c('copy', 'csv', 'excel'),
            columnDefs = list(
              list(className = 'dt-center', targets = "_all")),
            pageLength = 20
          ),
          class = "cell-border hover"
        )
    })
    
  })
  

# Chronic Fund Data -------------------------------------------------------
  observeEvent(input$sidebarItemExpanded == "chronic", {
    
    # Fetch data from the "Medicine " table
    output$medicine_table <- renderDT({
      dbReadTable(conn, "Chronic_Fund") |>
        datatable(
          escape = FALSE,
          extensions = 'Buttons',
          rownames = FALSE,
          filter = 'top',
          options = list(
            searching = TRUE,
            paging = TRUE,
            bInfo = FALSE,
            scrollX = TRUE,
            autoWidth = TRUE,
            dom = 'tB',
            buttons = c('copy', 'csv', 'excel'),
            columnDefs = list(
              list(className = 'dt-center', targets = "_all")),
            pageLength = 20
          ),
          class = "cell-border hover"
        )
    })
    
  })
  }

# Run the application 
shinyApp(ui = ui, server = server)
