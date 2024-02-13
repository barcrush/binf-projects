library(shiny)
library(shinyWidgets)

ui <- fluidPage(
  shinyWidgets::sliderTextInput(inputId = 'num', label = 'Select a perplexity value',
                                choices = c(15,30,45,60,85,100), grid = T),
  plotOutput("scatter")
)