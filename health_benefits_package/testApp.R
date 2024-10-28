
# Load the required libraries
source('global.R')

# Define the UI 
ui <- dashboardPage(
  dashboardHeader(title = "Health Essential Benefits Package Dashboard"),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Home", tabName = "home", icon = icon("home"), selected = TRUE),
      menuItem("Conditions tables", tabName = "conditions")
    )
  ),
  
  dashboardBody(
    tags$head(
      tags$style(HTML("
        .table > tbody > tr.selected {
          background-color: orange;  /* Change selected row color */
        }
        .table {
          margin-bottom: 20px;  /* Space between tables */
        }
      "))
    ),
    
    tabItems(
      tabItem(tabName = "home",
              h2("Welcome to the Essential Benefits Package Dashboard"),
              p("The dashboard allows you to explore the different essential medical packages. Use the navigation bar to select a table and view its contents."),
              tags$img(src = "https://media.istockphoto.com/id/1480239160/photo/an-analyst-uses-a-computer-and-dashboard-for-data-business-analysis-and-data-management.jpg?s=612x612&w=0&k=20&c=Zng3q0-BD8rEl0r6ZYZY0fbt2AWO9q_gC8lSrwCIgdk=", height="auto", width = "100%")
      ), 
      tabItem(
        tabName = "conditions",
        fluidRow(
          column(4,
                 selectInput(
                   inputId = "conditions",
                   label = "Select data:",
                   choices = dbListTables(conn),
                   selected = dbListTables(conn)[1]
                 )
                 
          ),
          column(
            8,
            dataTableOutput("conditions_table", width = "100%")
          )
        )
      )
      
      
    )
  )
)


# Define server logic
server <- function(input, output, session) {
  
  observeEvent(input$conditions, {
    selected_table <- input$conditions
    output$conditions_table <- renderDT({
      dbReadTable(conn, selected_table) %>% 
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
            pageLength = 10
          ),
          class = "cell-border hover"
        ) 
      
    })
    
  })
  
  onStop(function() {
    dbDisconnect(conn)
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)
