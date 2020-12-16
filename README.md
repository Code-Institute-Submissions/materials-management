# [Materials Management](https://materials-mgnt.herokuapp.com)


* The main purpose of this web app is to simulate a Materials Management System in a pen factory;
* It respects the concept of pull production: Stock and Inventory levels are considered buffers for customers demand and supply variability, whereas all other processes only happens when they are requested and in the quantity requested;

----------------------------------------------------------------------------------------------------------------------------------------

# User Experience - UX 

Although it is possible to do all the tasks, in real life each sector would be responsible for their own requests. It also takes in consideration that none of the processes are automated so that all the requests would need to be placed manually.

- ## User stories
  
    - ## Sales Department
      - I would like to check the stock level daily, knowing how much material is available and how many is in production, so that I can plan and schedule better my sales.
    
    - ## Stock Department
      - I would like to keep the stock level balanced, and always trying to attend the so variable customer demand. When I see that the stock level is low, I would like to have the authority to just request more to cover it.
     
    - ## Production Department
      - I do not want to be under pressure of sales constantly, the demand varies a lot and I have difficulty to plan and schedule the production.
    
    - ## Inventory Department
      - I would like to have a broader view of the production and supply. It is difficult to always try to fit the production schedule that each time has a different priority.


- ## Design

  - ### Colour Scheme
    - The main background colour throughout the website is light grey with titles and navigation bars dark purple, while the font is white;
    - It is designed to keep the same structure throught all navigation, thus the user will not have the impression that is being redirected to different pages;

  - ### Typography
     - It was used the standard font and no special style was applied.

---------------------------------------------------------------------------------------------------------------------------------------

# Features

- Responsive design allows the system to be used in any device, with certain limitation for small ones due to the amount of tables on it
- Interactive list of items when adding materials, items in purchase or placing new orders. Items can be removed and only the remaining ones will be sent over to the database.
  
----------------------------------------------------------------------------------------------------------------------------------------

# Technologies Used

## Languages Used

-   [HTML5](https://en.wikipedia.org/wiki/HTML5)
-   [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
-   [JAVASCRIPT](https://en.wikipedia.org/wiki/JavaScript)]
-   [PYTHON](https://en.wikipedia.org/wiki/Python_(programming_language))
-   [MONGODB](https://en.wikipedia.org/wiki/MongoDB)

## Frameworks, Libraries & Programs Used

1. [Materialize:](https://materializecss.com/)
    - Bootstrap was used to assist with positioning.
1. [Font Awesome 5.6.3:](https://fontawesome.com/)
    - Font Awesome was used to style the dice, trophy and star on the board.
1. [Git](https://git-scm.com/)
    - Git was used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub.
1. [GitHub:](https://github.com/)
    - GitHub is used to store the projects code after being pushed from Git.

---------------------------------------------------------------------------------------------------------------------------------------

# Testing

The W3C Markup Validator and W3C CSS Validator Services were used to validate every page of the project to ensure there were no syntax errors in the project.

-   [W3C Markup Validator](https://jigsaw.w3.org/css-validator/#validate_by_input)
-   [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input)


- ## Testing User Stories from User Experience (UX) Section

  - ## Orders Department
    - A user from sales department would have knowlodge of the customer demand. Therefore would have the responsibility to add new orders. Entering customer data and selecting a list of products to the new order;
    - The registered products are listed and one order can have more than one product;
    - Before confirming the new order, the user can add and remove items from the order list;
    - When the order is confirmed, the user is redirected to the Customer Orders list where he/she can see the new order placed;
    - In the Customer Orders list, the user can see the details of each order;
    - The Order Details shows the quantity of each item requested in this order as well as the quantity available in stock;
    - The order can only be shipped if there are all materials available in stock;
    - It is also possible to drill-down and see the details and status of each product in the order.
    
  - ## Stock Department
    - A user from stock department has a wider vision of each product, the stock level as well as the quantity of each material in orders request and production;
    - Based on the stock policy, the user is able to request the production of each product in order to keep the desired stock level;
    - After confirming, the user is redirected to the Production Orders list;
    - As in the Orders List, it is also possible to drill-down in the Production Orders list and see its status.
    
  - ## Production Department
    - For each Production Request, the user will need to send a Material Request Order to the Inventory Department, once the materials are available for production, the status of the Procuction Order will change from "Pending" to "Materials Received";
    - There is a short Order History thread that it is possible to see when the order was created, materials requested, materials available and production finished.
    - The user also can see the quantity requested and which materials the product is made of;
    - When the materials are requested, a Material Request is created;
    - In Materials Request details shows how many of each material was requested and the Inventory level, the request will have status "Pending" until all materials requested are available, when it can be approved for production.
    
  - ## Inventory Department
    - As in the Stock department, the user will have a wider vision, but now for materials: the inventory level and the quantity requested for production and in new purchases;
    - Each material has a drill-drow and it can be asign to a different supplier;
    - According to the production necessity and/or inventory policy, new purchases can be made.
    
  - ## Purchases
    - A new purchase can be made at any time, the user can choose the supplier and place a order to request new materials.
    - Once the order is received, the inventory level is updated.
    
  - ## Suppliers
    - The user has the possibility to add new Suppliers, edited or deleted, as well as the items that they sell.
    
  - ## Materials and Products
    - In order to register a new product, the user will need to register materials first.
    - A product can be made of materials and a pack of products, very common when you are looking for buy different colors of pen.


## Further Testing

-   The Website was tested on Google Chrome, Internet Explorer and Microsoft Edge browsers;
-   The website was viewed on a variety of devices such as Desktop in multiple screen sizes, iPad, iPad Pro, Samsumg Laptop, Moto G4, Galaxy S5, Xiaomi M3, Nokia 6, Pixel 2, Pixel 2XL, iPhone 5/SE, iPhone 6/7/8+Plus models and iPhoneX.

---------------------------------------------------------------------------------------------------------------------------------------

# Credits

-   This ReadMe file was based on a sample available on [Code Institute Solutions repositories](https://github.com/Code-Institute-Solutions)

-   Quick information of "how to" was promplty found on [W3Schools](https://www.w3schools.com/)

---------------------------------------------------------------------------------------------------------------------------------------- 

# Acknowledgements

-   My Mentor for continuous helpful feedback.

-   Code Institute video classes with its helpful content.

-   My wife, Cristina, who supported me pantiently in the long hours spent coding.
