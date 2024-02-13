# read in the data 
msne_15 <- read.table('adBrain_diffPerp/adBrain_multiSNE_15.txt', sep = ' ')
msne_30 <- read.table('adBrain_diffPerp/revised_adBrain_multiSNE.txt', sep = ' ')
msne_45 <- read.table('adBrain_diffPerp/adBrain_multiSNE_45.txt', sep = ' ')
msne60 <- read.table('adBrain_diffPerp/adBrain_multiSNE_60.txt', sep = ' ')
msne85 <- read.table('adBrain_diffPerp/adBrain_multiSNE_80.txt', sep = ' ')
msne_100 <- read.table('adBrain_diffPerp/adBrain_multiSNE_100.txt', sep = ' ')
adBrain_labels <- read.csv('adbrain_rna_labels.csv')
adBrain_labels <- as.vector(adBrain_labels[,2])

library(plotly)
library(dplyr)

msne1x <- msne_15[,1]
msne1y <- msne_15[,2]
df_1 <- data.frame('x1' = msne1x, 'y1' = msne1y)

msne2x <- msne_30[,1]
msne2y <- msne_30[,2]
df_2 <- data.frame('x2' = msne2x, 'y2' = msne2y)

msne3x <- msne_45[,1]
msne3y <- msne_45[,2]
df_3 <- data.frame('x3' = msne3x, 'y3' = msne3y)

msne4x <- msne60[,1]
msne4y <- msne60[,2]
df_4 <- data.frame('x4'=msne4x, 'y4' = msne4y)

msne5x <- msne85[,1]
msne5y <- msne85[,2]
df_5 <- data.frame('x5'=msne5x, 'y5'=msne5y)

msne6x <- msne_100[,1]
msne6y <- msne_100[,2]
df_6 <- data.frame('x6'=msne6x, 'y6' = msne6y)

final_df <- cbind(df_1, df_2, df_3, df_4, df_5, df_6, labels = factor(adBrain_labels))

interval <- 1/14

colors <- list(
  c(0, 'rgb(248, 118, 109)'),
  c(interval, 'rgb(229,135,0)'),
  c(2*interval, 'rgb(201,152,0)'),
  c(3*interval, 'rgb(163, 165,0)'),
  c(4*interval, 'rgb(107, 177,0)'),
  c(5*interval, 'rgb(0,186,56)'),
  c(6*interval, 'rgb(0, 191, 125)'),
  c(7*interval, 'rgb(0, 192, 175)'),
  c(8*interval, 'rgb(0, 188, 216)'),
  c(9*interval, 'rgb(0, 176, 246)'),
  c(10*interval, 'rgb(97, 156, 255)'),
  c(11*interval, 'rgb(185, 131, 255)'),
  c(12*interval, 'rgb(231, 107, 243)'),
  c(1, 'rgb(253,  97, 209)'))


steps <- list(
  list(args = list("visible", c(FALSE,TRUE,FALSE, FALSE, FALSE, FALSE)), 
       label = " 15", 
       method = "restyle", 
       value = "15"
  ),
  list(args = list("visible", c(FALSE,FALSE,TRUE, FALSE, FALSE, FALSE)), 
       label = "30", 
       method = "restyle", 
       value = "30"
  ),
  list(args = list("visible", c(FALSE,FALSE, FALSE, TRUE, FALSE, FALSE)), 
       label = "45", 
       method = "restyle", 
       value = "45"
  ),
  list(args = list("visible", c(FALSE,FALSE, FALSE, FALSE, TRUE, FALSE)), 
       label = "60", 
       method = "restyle", 
       value = "60"
  ),
  list(args = list("visible", c(FALSE, FALSE, FALSE, FALSE, FALSE, TRUE)), 
       label = "80", 
       method = "restyle", 
       value = "80"
  ),
  list(args = list("visible", c(TRUE, FALSE, FALSE, FALSE, FALSE, FALSE)),
       label = '100',
       method = 'restyle',
       value = '100')
)

x <- list(
  title = "multiSNE-1",
  zeroline = FALSE,
  showline = TRUE,
  showticklabels = FALSE,
  showgrid = FALSE
)

y <- list(range = -100:150,
          title = "multiSNE-2",
          zeroline = FALSE,
          showline = TRUE,
          showticklabels = FALSE,
          showgrid = FALSE
)



perp_plot <- plot_ly(data = final_df, type = 'scatter', mode = 'markers',
                 marker = list(size = 3)) %>%
  add_trace(x = ~x1, y = ~y1, marker = list(color = ~labels, colorscale=colors), name='15',showlegend = F) %>%
  add_trace(x = ~x2, y = ~y2,marker = list(color = ~labels, colorscale=colors), name='30',showlegend = F) %>%
  add_trace(x = ~x3, y = ~y3,marker = list(color = ~labels, colorscale=colors), name ='45',showlegend = F)%>%
  add_trace(x = ~x4, y = ~y4,marker = list(color = ~labels, colorscale=colors), name = '60',showlegend = F)%>%
  add_trace(x = ~x5, y = ~y5,marker = list(color = ~labels, colorscale=colors), name = '80',showlegend = F) %>%
  add_trace(x = ~x6, y = ~y6,marker = list(color = ~labels, colorscale=colors), name = '100',showlegend = F) %>%
  layout(
    sliders = list(
      list(
        active = 0, 
        currentvalue = list(prefix = "Slide the bar to change the perplexity value<br> Perplexity = "), font = list(size = 10), 
        pad = list(t = 60), 
        steps = steps)),
    xaxis = x, 
    yaxis = y,
    title = 'Multi-SNE visualisation of SNARE-seq data from mouse brain, with varying perplexity', font = list(size = 6)) %>%
  style(hoverinfo = 'none') %>%
  config(displayModeBar = FALSE)

perp_plot