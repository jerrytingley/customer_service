# COM-100 Honors Project

The Django project was written as an Honors project for my COM-100 class. 

# Overview

Companies have realized that a large portion of their customer base is on Twitter. In order to
better serve these customers, many of these companies provide a customer service presence on Twitter
to help their Twitter using customers with any problems that they may be having with the companies product or service.
Custom software was written to poll the top four popular customer service accounts and pull out the conversations they were
having with customers. For there, features were pulled from each conversation to a generate a dataset that was then
used to train a logisitc regression model. This model is used to determine the probability that a conversation will yield
a positive correspondence based on the first Tweet as well as the probability that the user will respond at all to the
customer service account. It's up to assign meaning to this data. For example, a company may choose to quickly respond to
potential conversations that more likely to be negative or visa versa.
