# Database Schema 

## Users

| Field Name | Data Type | Constraints | Reasoning |
| :--- | :--- | :--- | :--- |
| id | UUID (v7) | Primary Key  | Secure, non-enumerable and time sorted for index efficiency |
| username | VarChar(255) | Not Null, Unique | Core requirements for search and display |
| password | VarChar(255) | Not Null, Hashed | Core requirements for auth |
| email | VarChar(255) | Not Null, Unique | Core requirements for further feature development |
| is_reader | Boolean | Not Null | Check if a reader |
| is_author | Boolean | Not Null | Check if a writer |


## Posts

| Field Name | Data Type | Constraints | Reasoning |
| :--- | :--- | :--- | :--- |
| id | UUID (v7) | Primary Key  | Secure, non-enumerable and time sorted for index efficiency |
| author_id | UUID (v7) | Foreign Key (Users.id) | Indexed. Link the author with the post |
| title | VarChar(255) | Not Null | Core requirements for search and diplay |
| content | Text | Not Null | Core requirements for search and diplay |
| content_html | 
| status | Enum | Default: 'Draft' | Enum: Draft, Published, Archived |
| slug | VarChar (255) | Unique, Indexed | For faster search and filter |
| search_vector | TSVector | GIN Indexed | For full text search feature |
| comment_count | Int | Not Null | Denormalized if have to count number of comment per post |
| created_at | DateTime | Not Null, Default:  'Today' | N/A |
| updated_at | DateTime | Not Null, Default: 'Today' | N/A |
| deleted_at | DateTime | Nullable | N/A | 

| 
## Comments

| Field Name | Data Type | Constraints | Reasoning |
| :--- | :--- | :--- | :--- |
| id | UUID (v7) | Primary Key  | Secure, non-enumerable and time sorted for index efficiency |
| post_id | UUID (v7) | Foreign Key (Posts.id) | Indexed, CASCADE -> Delete all the comments associated with a deleted post |
| user_id | UUID (v7) | Foreign Key (Users.id) | Indexed, PROTECTED -> Keep all the comments associated with a deleted user |
| message | Text | Not Null | Required not null to be displayed |
| created_at | DateTime | Not Null, Default:  'Today' | N/A |
| updated_at | DateTime | Not Null, Default: 'Today'  | N/A |
| deleted_at | DateTime | Nullable | N/A | 

**Note:**
- Soft Delete Tax: Every GET query now must include WHERE delete_at IS NULL. Fix: CustomerManager in Django and add composite index for `(post_id, deleted_at, created_at)` for Commentsentity and `(slug, deleted_at)` for Posts entity. 
- About Comment Count: Trading Data Integrity for Read Speed. There are two methods - override the save of Comments (refered), increase the posts.comment_count by 1, using Django Signal. 