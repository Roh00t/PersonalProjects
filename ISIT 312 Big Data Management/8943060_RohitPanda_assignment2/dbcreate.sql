CREATE TABLE AUTHOR(
A_ID 		NUMERIC(10) 	NOT NULL, /* Unique author ID		*/
A_FNAME 	VARCHAR(20) 	NOT NULL, /* First name of author	*/
A_MNAME		VARCHAR(20)	NOT NULL, /* Last name of author	*/
A_LNAME 	VARCHAR(20) 	NOT NULL, /* Middle name of author	*/
A_DOB		DATE		NOT NULL, /* Date of birth of author	*/
A_BIO		VARCHAR(500)	NOT NULL, /* About the author		*/
	CONSTRAINT AUTHOR_PKEY PRIMARY KEY (A_ID),
	CONSTRAINT AUTHOR_CHECK1 CHECK(A_ID > 0) );		

CREATE TABLE ITEM(
I_ID	 	NUMERIC(10) 	NOT NULL, /* Unique ID of item		*/
I_TITLE	 	VARCHAR(60) 	NOT NULL, /* Title of item		*/
I_A_ID	 	NUMERIC(10) 	NOT NULL, /* Author ID of item		*/
I_PUB_DATE	DATE 		NOT NULL, /* Date of release of an item */
I_PUBLISHER 	VARCHAR(60) 	NOT NULL, /* Publisher of item		*/
I_SUBJECT 	VARCHAR(60) 	NOT NULL, /* Subject of book		*/
I_DESC 		VARCHAR(500) 	NOT NULL, /* Description of item	*/
I_RELATED1	NUMERIC(10)	NOT NULL, /* Unique item ID (I_ID) of related item */
I_RELATED2      NUMERIC(10)     NOT NULL, /* Unique item ID (I_ID) of related item */
I_RELATED3      NUMERIC(10)     NOT NULL, /* Unique item ID (I_ID) of related item */
I_RELATED4      NUMERIC(10)     NOT NULL, /* Unique item ID (I_ID) of related item */
I_RELATED5      NUMERIC(10)     NOT NULL, /* Unique item ID (I_ID) of related item */
I_THUMBNAIL 	VARCHAR(10),		  /* Pointer to thumbnail image of item */
I_IMAGE		VARCHAR(10),		  /* Pointer to  image of item 	*/
I_SRP 		NUMERIC(15,2) 	NOT NULL, /* Suggested retail price	*/
I_COST 		NUMERIC(15,2) 	NOT NULL, /* Cost of item		*/
I_AVAIL 	DATE 		NOT NULL, /* When item is available	*/
I_STOCK		NUMERIC(4)	NOT NULL, /* Quatity in stock		*/
I_ISBN 		CHAR(13) 	NOT NULL, /* Product ISBN		*/
I_PAGE 		NUMERIC(4) 	NOT NULL, /* Number of pages of  book	*/
I_BACKING 	VARCHAR(15) 	NOT NULL, /* Type of book:paper,hardback */
I_DIMENSIONS 	VARCHAR(25) 	NOT NULL, /* Size of book in inches	*/
	CONSTRAINT ITEM_PKEY PRIMARY KEY (I_ID),
	CONSTRAINT ITEM_FKEY FOREIGN KEY (I_A_ID)
		REFERENCES AUTHOR(A_ID),
	CONSTRAINT ITEM_CHECK1 CHECK(I_ID > 0),
	CONSTRAINT ITEM_CHECK2 CHECK(I_A_ID > 0) );		
