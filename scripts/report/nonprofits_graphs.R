points = read.csv(file="nonprofits.csv",head=T,sep=",", quote="\"", na.strings=c(""))



library(ggplot2)

my_theme = function() { 
  return (  
    theme(
      axis.text.y = element_text(size = rel(1.7)),
      axis.text.x = element_text(size = rel(1.7)),
      axis.title.y = element_text(size = rel(1.7)),
      axis.title.x = element_text(size = rel(1.7)),
      plot.title = element_text(size = rel(2)),
      legend.text= element_text(size = rel(2)),
      panel.background = element_rect(fill="white"),
      panel.grid.major.x = element_blank(),
      panel.grid.minor.x = element_blank(),
      panel.grid.major.y = element_line(color="#cbced9"),
      panel.grid.minor.y = element_line(color="#cbced9")
    )
  )
}

ggplot(
  data=points,
  aes(x=ntee)
) + 
  geom_bar(    
    stat = 'bin',
    position = 'stack', 
    fill="#599ad3",
    #na.rm=T
  ) + xlab("NTEE code") + my_theme()
  
  