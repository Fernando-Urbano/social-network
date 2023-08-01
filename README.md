# Social Network
This is project number 4 of the CS50 Web Development course with Django and JavaScript lectured by Harvard CS department.

## Screencast of project

## New Post
Users who are signed can to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

<img width="644" alt="image" src="https://github.com/Fernando-Urbano/cs50w-p4-network/assets/99626376/c269f154-2be0-49a7-a18e-e7d28fa84cc5">

## All Posts
The “All Posts” link in the navigation bar takes the user to a page where they can see all posts from all users, with the most recent posts first.

Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has.

<img width="953" alt="image" src="https://github.com/Fernando-Urbano/cs50w-p4-network/assets/99626376/4f959338-c01a-4a14-bda6-ef1de5208e82">

## Profile Page
Clicking on a username should load that user’s profile page. This page:
- Display the number of followers the user has, as well as the number of people that the user follows.
- Display all of the posts for that user, in reverse chronological order.
- For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user is not be able to follow themselves.

![image](https://github.com/Fernando-Urbano/cs50w-p4-network/assets/99626376/46b8cd6a-535a-4e39-997f-c4bd18683ee8)

## Following
The “Following” link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
- This page behaves just as the “All Posts” page does, just with a more limited set of posts.
- This page is only be available to users who are signed in.

![image](https://github.com/Fernando-Urbano/cs50w-p4-network/assets/99626376/3dfaddd6-288d-43eb-b04f-27b427344c20)

## Pagination
On any page that displays posts, posts are displayed 10 on a page. If there are more than ten posts, a “Next” button appears to take the user to the next page of posts (which is older than the current page of posts). If not on the first page, a “Previous” button appears to take the user to the previous page of posts as well.

![image](https://github.com/Fernando-Urbano/cs50w-p4-network/assets/99626376/ec108351-289c-4a8d-aaeb-98877fdbee18)

