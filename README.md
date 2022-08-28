# Wine Recommender App through wine features analysis plus visualization
_Masters Thesis Project_
_University of Barcelona, Master in Foundations of Data Science_

## About this Repository

This is the master repository for the thesis project 'Wine Characteristics Analysis using ML to build a Wine Recomender App', authored by Marc Garcia and Herman Dempere.

This project and it's course are part of the Masters in Fundamental Principles of Data Science, at the University of Barcelona.

## Abstract

This is a project of applied data analysis that consist on deploying a wine web application that its main objective is to recommend catalan wines to non-expert users to introduce them in an effortless manner in complex and fascinating world. 

To get the data several data sources has been analyzed and a scrapping algorithm has been implemented. 

To recommend similar wines based on a wine that the user already liked a content based recommender, based on specific wine pre-processed features, will be trained. Secondly to the interviewed experts this CBR is outperforming by far the recommendations from the most well known Spanish wine guide. Several algorithms has been tested and optimized to predict the wine zone based on the user taste.

In order to synthesize the number of wine features, that confuses non expert users, an autoencoder has been implemented. To visualize these synthesized features and help the user to navigate through the recommendation several wine visualization have been implemented with the focus on a novel exploration tool for wine graph recommendations.

The notebooks and the codes of this project can be found in:

https://github.com/Nerucius/2022.tfm.winedb


Finally, everything has been deployed in a production server, you can find the url:

https://winedb.hdempere.me/

## Contained in this Repository

- `\djando` : Source code for the wine recommender application.
- `\notebooks` : Jupyter notebooks with the machine learning algorithms used in the project.