library(shiny)
library(ggplot2)

## load in the data returned from multi-SNE algorithm 
msne_15 <- read.table('./data/adBrain_multiSNE_15.txt', sep = ' ')
msne_30 <- read.table('./data/adBrain_multiSNE_39.txt', sep = ' ')
msne_45 <- read.table('./data/adBrain_multiSNE_45.txt', sep = ' ')
msne_60 <- read.table('./data/adBrain_multiSNE_60.txt', sep = ' ')
msne_85 <- read.table('./data/adBrain_multiSNE_80.txt', sep = ' ')
msne_100 <- read.table('./data/adBrain_multiSNE_100.txt', sep = ' ')
adBrain_labels <- read.csv('./data/adbrain_rna_labels.csv') # true labels (cell type) for each data point 
adBrain_labels <- as.vector(as.factor(adBrain_labels[,2]))

msne_list <- list(msne_15, msne_30, msne_45, msne_60, msne_85, msne_100)
names(msne_list) <- c("15", "30", "45", "60","85","100")

server <- function(input, output){
  perp <- reactive({as.data.frame(eval(parse(text = paste('msne_list$', '`', input$num, '`', sep = ''))))})
  x <- reactive({eval(parse(text = paste('msne_list$', '`', input$num, '`','[,1]', sep = '')))})
  y <- reactive({eval(parse(text = paste('msne_list$', '`', input$num, '`','[,2]', sep = '')))})
  
  output$scatter <- renderPlot({ggplot(data = perp())+
      geom_point(aes(x=x(),y=y(), color = adBrain_labels))+
      labs(x = 'MultiSNE-1', y = 'MultiSNE-2', title = paste0('Multi-SNE visualisation of adult mouse brain SNARE-seq data, with perplexity ', as.character(input$num)))+
      theme(plot.title = element_text(hjust = 0.5))+
      theme_classic()+
      scale_colour_discrete(name = 'Clusters')})

}
