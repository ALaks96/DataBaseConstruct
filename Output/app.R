library(shiny)
library(dplyr)
library(tidyverse)
library(shinythemes)
library(plotly)
library(shinythemes)
library(ggplot2)

ur_path <- glue::glue(getwd(), "/metadata.csv")
don <- read_csv(ur_path, col_types = list(col_double(), 
                                          col_character(), 
                                          col_character(), 
                                          col_character(), 
                                          col_datetime(), 
                                          col_datetime(), 
                                          col_character(), 
                                          col_double())) %>% 
  select(-X1) %>% 
  rename(authors = `Authors`,
         created_date = `Created_Date`,
         last_mod_by = `Last_Modified_By`,
         modified_date = `Modified_Date`,
         title = Title,
         location = Location,
         conformity = Conformity) %>% 
  na.omit()

cre <- don %>% 
  select(title, created_date, authors, conformity) %>% 
  rename(date = created_date, 
         author = authors)
mod <- don %>% 
  select(title,modified_date, last_mod_by, conformity) %>% 
  rename(date = modified_date, 
         author = last_mod_by)

viz_don <- cre %>% 
  rbind(mod)

people <- unique(viz_don$author)
files <- unique(viz_don$title)


ui <- fluidPage(theme = shinytheme('sandstone'),
                title = 'BlueTeam',
                
                navbarPage(tags$strong("Metadata Visualisation"),
                           
                           tabPanel('File tracker',
                                    sidebarPanel(
                                      selectInput('Files',
                                                  "Choose the files you're interested in!",
                                                  choices = files,
                                                  selected = "20190413_CONF_FHQ_007_FRAGO_TANGO HARVEST.pdf",
                                                  multiple = TRUE),
                                      sliderInput('plotHeight',
                                                  'Adjust the height of the plot', 
                                                  min = 100,
                                                  max = 5000,
                                                  value = 900),
                                      sliderInput('plotWidth',
                                                  'Adjust the width of the plot',
                                                  min = 100,
                                                  max = 5000,
                                                  value = 1200)),
                                    mainPanel(plotlyOutput("filemetadata", width = "150%", height = "20%"),
                                              DT::dataTableOutput(outputId = "filetable"))
                           ),
                           tabPanel('People tracker',
                                    sidebarPanel(
                                      selectInput('Author',
                                                  "Choose the people you're interested in!",
                                                  choices = people,
                                                  selected = "ASCIONE Thibault CBA",
                                                  multiple = TRUE),
                                      sliderInput('plotHeight2',
                                                  'Adjust the height of the plot', 
                                                  min = 100,
                                                  max = 5000,
                                                  value = 900),
                                      sliderInput('plotWidth2',
                                                  'Adjust the width of the plot',
                                                  min = 100,
                                                  max = 5000,
                                                  value = 1200)),
                                    mainPanel(plotlyOutput("peoplemetadata", width = "150%", height = "20%"),
                                              DT::dataTableOutput(outputId = "peopletable"))
                           ),
                           tabPanel('Conformity tracker',
                                    sidebarPanel(
                                      selectInput('Files2',
                                                  "Choose the files you're interested in!",
                                                  choices = files,
                                                  selected = c("OHQ ALL - FRAGO.docx","20190413_CONF_FHQ_007_FRAGO_TANGO HARVEST.pdf"),
                                                  multiple = TRUE),
                                      sliderInput('plotHeight3',
                                                  'Adjust the height of the plot', 
                                                  min = 100,
                                                  max = 5000,
                                                  value = 900),
                                      sliderInput('plotWidth3',
                                                  'Adjust the width of the plot',
                                                  min = 100,
                                                  max = 5000,
                                                  value = 1200)),
                                    mainPanel(plotlyOutput("conformity",  width = "150%", height = "20%"),
                                              DT::dataTableOutput(outputId = "conformitytable"))
                           )
                )
)





# Define server logic
server <- function(input, output) {
  
  ################### FILE METADATA ######################
  
  # file_data <- reactive({
  #   don %>%
  #     filter(title %in% input$Files & last_mod_by %in% input$Author & authors %in% input$Author)
  # })
  
  file_data_viz <- reactive({
    viz_don %>%
      filter(title %in% input$Files)
  })
  
  # output$filemetadata <- renderPlotly({
  #   p <- ggplot(data = file_data(),
  #               aes_string(y = as.factor(file_data()$title),
  #                          x = file_data()$created_date,
  #                          color = as.factor(file_data()$authors))) +
  #     geom_point() +
  #     geom_line(group = as.factor(file_data()$authors)) +
  #     geom_point(aes_string(y = as.factor(file_data()$title),
  #                           x = file_data()$modified_date,
  #                           color = as.factor(file_data()$last_mod_by),
  #                           group = as.factor(file_data()$last_mod_by))) +
  #     geom_line(aes_string(y = as.factor(file_data()$title),
  #                          x = file_data()$modified_date,
  #                          color = as.factor(file_data()$last_mod_by),
  #                          group = as.factor(file_data()$last_mod_by))) +
  #     theme_bw() +
  #     xlab("Date") +
  #     ggtitle("File metadata tracking") +
  #     theme(axis.text.y = element_text(angle = 45))
  #   
  #   ggplotly(p,
  #            height = input$plotHeight,
  #            width = input$plotWidth,
  #            opacity = 0.6)
  # })
  
  output$filemetadata <- renderPlotly({
    p <- ggplot(data = file_data_viz(),
                aes_string(y = as.factor(file_data_viz()$title),
                           x = file_data_viz()$date,
                           color = as.factor(file_data_viz()$author),
                           #group = as.factor(file_data_viz()$title),
                           size=2,
                           alpha = 0.6)) +
      geom_point() +
      geom_line() +
      theme_bw() +
      xlab("Date") +
      ggtitle("File metadata tracking") +
      theme(axis.text.y = element_blank())
    
    ggplotly(p,
             height = input$plotHeight,
             width = input$plotWidth,
             opacity = 0.6)
  })
  
  output$filetable <- DT::renderDataTable({
    don %>%
      filter(title %in% input$Files)
  })
  
  ################### PEOPLE METADATA ######################
  
  people_data_viz <- reactive({
    viz_don %>%
      filter(author %in% input$Author)
  })
  
  output$peoplemetadata <- renderPlotly({
    pp <- ggplot(data = people_data_viz(),
                 aes_string(y = as.factor(people_data_viz()$title),
                            x = people_data_viz()$date,
                            color = as.factor(people_data_viz()$author),
                            #group = as.factor(people_data_viz()$title),
                            size=2,
                            alpha = 0.6)) +
      geom_point() +
      geom_line() +
      theme_bw() +
      xlab("Date") +
      ggtitle("File metadata tracking") +
      theme(axis.text.y = element_blank())
    
    ggplotly(pp,
             height = input$plotHeight2,
             width = input$plotWidth2,
             opacity = 0.6)
  })
  
  output$peopletable <- DT::renderDataTable({
    don %>%
      filter(last_mod_by %in% input$Author & authors %in% input$Author)
  })
  
  ###################### CONFORMITY #########################
  
  conformity_data_viz <- reactive({
    don %>%
      filter(title %in% input$Files2) %>% 
      arrange(desc(conformity))
  })
  
  output$conformity <- renderPlotly({
    print(ggplotly(ggplot(data = conformity_data_viz(),
                 aes(y = conformity_data_viz()$conformity,
                            x = as.factor(conformity_data_viz()$title),
                            fill = as.factor(conformity_data_viz()$authors),
                            alpha = 0.6)) +
      geom_col() +
      theme_bw() +
      xlab("File") +
      ylab("Conformity to canevas") +
      ggtitle("Conformity tracking") +
      theme(axis.text.x = element_text(angle = 45)),
      height = input$plotHeight3,
      width = input$plotWidth3))

  })
  
  output$conformitytable <- DT::renderDataTable({
    conformity_data_viz() %>% 
      select(title, authors, conformity)
                           
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)