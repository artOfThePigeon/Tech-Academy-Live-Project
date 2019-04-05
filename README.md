![image'](https://github.com/CreativeDave/Tech-Academy-Live-Project/blob/master/media/TTATitle.png)
---
> A forum for The Tech Academy built in django with my classmates.
## Project Overview
Over the course of 2 weeks, we held daily standups and built the foundation of an exciting forum for the next generation of Tech Academy students to complete. This was a great opportunity to practice SCRUM methodology with other students, and learn how Azure Devops is used in the real world. After creating our own branch, we would recieve our tasks from the devops board and then commit our changes in visual studio using git version control.

### My Tasks
> My specific tasks were to edit the templates of the home/forum and the post page. This meant I had to design a way for the posts to sensibly display in the correct page containers and update as new threads and posts were added. 

- [Post Page](#Post-Page)
- [Home Page](#Home-Page)

![alt text](https://github.com/CreativeDave/Tech-Academy-Live-Project/blob/master/media/demo1.gif)

### Post-Page

In order to accomplish the task of having comments display as sub-sections of the thread title, and the comment box as a subsection of the comment section, I separated the template into 3 different containers, with each one utilizing django's 'include' tag to call the appropriate templates. This creates a clean looking template with only the important code being displayed. 
```
{% block content %}

  <div class=thread-container>
          
      {% include "forum/thread_header.html" %}

      <div class="post-comments">
          <hr style="height: 6px;background: url(http://ibrahimjabbari.com/english/images/hr-11.png)repeat-x 0 0;border: 0; margin:20px 0px 20px 0px">
          
          {% include "forum/comment_section.html" %}

      </div>
      <div class="leave-comment">
          <hr style="height: 6px;background: url(http://ibrahimjabbari.com/english/images/hr-11.png)repeat-x 0 0;border: 0; margin:20px 0px 20px 0px">
          
          {% include "forum/comment.html" %}

      </div>
  </div>
  
{% endblock %}
```
You can view the full code of each template, [thread_header.html](/Templates/forum/thread_header.html), [comment_section.html](/Templates/forum/comment_section.html), and [comment.html](/Templates/forum/comment.html).

##### To illustrate clearly from top to bottom how this works, let's look at the body of base.html. 

```
        
<div class="forum-container">

  <div class="navbar">

      {% include "partials/navbar.html" %}

  </div>

  <div class="main">

      {% block header %}{% endblock %} 

      <div class="container-post"> 

        {% block content %}{% endblock %}

      </div>

  </div>

</div>

 ```
As you can see, the div 'forum-container' has within it the div 'main.' The {block content} is within that. The CSS defines the grid layout of forum-container with 'main' being where you would expect it, the main section.
```
.forum-container {
    display: grid;
    grid-auto-rows: auto;
    grid-template-columns: auto;
    grid-template-areas:
        "navbar navbar navbar"
        "lside main rside"
        "footer footer  footer";
    grid-gap: .50em; 
}
```
Everything within the div main will be right in the center of the page. 

From the first bit of code I pasted, you can see the {block content} tag designates thats where all the subsequent content will be placed. Also within that first bit of code, you'll see 'forum/thread_header.html' included. Within that template, notice the div class 'post-body': 
```
<div class="post-body">
        <div>
            <h2><b>{{ thread.ThreadTitle }}</b></h2>
            <p style=>{{ thread.DateStarted }}</p>
    </div>
    <div>
        </br>
        <h3>{{ thread.ThreadBody }}</h3>
    </div>
 ```   
The CSS below defines it beginning at row 1, column 2. So, within the 'main' section, its at the top and 1 column over to the right. (The first column is the post's user profile information).
```
.post-body { 
    grid-area: 1 / 2 / span 1 / span 7; 
}
```
This doesn't define the comment section however, only the initial thread's content. 

The 'post-comments' section comes next, and is clearly defined in the CSS as: 
```
.post-comments { 
    grid-column-start: 2;
    grid-row-start: 2;
    grid-column-end: 7;
}
```
Meaning, within the main section of the grid, beginning on row 2, just below the body of the initial post, with the commentor's profile info beginning on column 2 (1 over from the poster's profile info), and spanning 7 columns. So, the first comment is on row 2, the second is on row 3, the third on 4... But this doesn't account for the proper placement of new comments.

To acheive this, within the forum/comment_section.html (the 2nd section of the post-page code I pasted) I wrote:
```
<div>
    <h3>Comments:</h3>
    <br>
</div>

    {% for comment in comments %}

<div class="auto-comment-container">  
<div class="post-side">
    <img src="{{ comment.User.userprofile.Avatar.url }}" alt="{{ comment.User.username }} Avatar" width="100">
    <p>{{ comment.User.username }}</p>
    <p>{{ comment.User.userprofile.Signature}}</p>
    <p>{{ comment.DateCreated }}</p>
</div>
<div class="post-body">
    <p>{{ comment.CommentBody }} </p>
</div>
</div>

    {% endfor %}
 ```
Notice the 'auto-comment container.' This is how I got all of future user comments to display in the proper relation to the other sections.  It took a couple tries to get the new posts to format properly, but eventually it was the ``` grid-auto-flow: row ``` property that did the trick.
```
.auto-comment-container {
    grid-gap: 5px;
    padding: 5px;

    display: grid;
    grid-auto-flow: row;
    grid-template-columns:1fr 8fr;
    grid-template-areas: 
        "side body";

}
```

I only defined two sections, 'side' for user profile information and 'body' for the post itself. When a user submits a comment, it auto-generates a new row for itself, continuing the patter, without moving over in columns. 

### Home-Page

