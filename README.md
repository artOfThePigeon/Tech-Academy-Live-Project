![image'](https://github.com/CreativeDave/Tech-Academy-Live-Project/blob/master/media/TTATitle.png)

> A forum for The Tech Academy built in django with my classmates.
## Project Overview
Over the course of 2 weeks, we held daily standups and built the foundation of an exciting forum for the next generation of Tech Academy students to complete. This was a great opportunity to practice SCRUM methodology with other students, become very familiar with git version control, and learn how Azure Devops is used in the real world. After creating our own branch, we would recieve our tasks from the devops board and then commit our changes in Visual Studio.

### My Tasks
> My specific tasks were to edit the templates of the home page and the post page. This meant I had to design a way for the posts to sensibly display in the correct page containers and update as new threads and posts were added. 

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
The div 'forum-container' has within it the div 'main.' The {% block content %} tag is within that. This is where every page will start to render content. The CSS defines the grid layout of 'forum-container' with 'main' being where you would expect it, the center of the page.
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
> Everything within the div 'main' will be right in the center of the page. In this case, nothing is defined for 'lside' and 'rside' so it consumes the entire viewport beneath the navbar. 

!['image'](https://github.com/CreativeDave/Tech-Academy-Live-Project/blob/master/media/post-page1.png)

From the first bit of code I pasted, you'll see 'forum/thread_header.html' is included using a template tag. If we look at a snippet of code from that template, there's a div class 'post-body': 
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
The CSS below defines it beginning at row 1, column 2. So, within the 'main' section, its at the very top, and 1 column over to the right. (The first column is the post's user profile information).
```
.post-body { 
    grid-area: 1 / 2 / span 1 / span 7; 
}
```
This doesn't define the comment section however, *only the initial thread's content.* 

For this, the 'post-comments' div was coded next, and is clearly defined in the CSS as: 
```
.post-comments { 
    grid-column-start: 2;
    grid-row-start: 2;
    grid-column-end: 7;
}
```
Translated, content rendered under this div is falls within the 'main' section of the grid, beginning on row 2, just below the body of the initial post, with the commentor's profile info beginning on column 2 (1 over from the poster's profile info), and spanning 7 columns... 

So, the first comment is on row 2, the second is on row 3, the third on 4... *But this doesn't account for the proper placement of new comments.*

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

I only defined two sections, 'side' for user profile information and 'body' for the post itself. When a user submits a comment, it auto-generates a new row for itself, continuing the pattern without moving over in columns. 

### Home-Page
Similar to the post-page, the home-page needed a way for all new posts to display properly in the container without overflowing onto a new column. The inital template is simple and clean looking, thanks to django's template tags. 

```
{% block content %}

<div class="subject-head">
	<h3>Recent posts</h3>
</div>

{% for thread in threads %}

	<div class="auto-post">
		<div class="lcol">
			<p>📄</p>
			<p>last active: {{ thread.DateUpdate }}</p>
		</div>
		<div class="rcol">
			<a href="{% url 'Forum:thread' thread.id %}">{{ thread.ThreadTitle }}</a>
		</div>
			
	</div>

{% endfor %}

{% endblock %}
```



Again I chose to use the ```grid-auto-flow: row;``` property, but this time I defined length and width with pixels, instead of the 'fr' measure. Everytime a new thread is created, it will create a new row in the 'main' section. This is defined by the 'auto-post' class in the CSS.

```
.auto-post {
    display: grid;
    padding-left: 5px;
    grid-auto-flow: row;
    grid-template-rows: 100px ;
    grid-gap: 20px;
    grid-template-columns: 100px 600px;
    text-align: left;
    border-left: 27px solid rgba(28,110,164,0.3);
    border-radius: 10px 0px 0px 10px;
    margin-bottom:10px;
    padding-bottom:2px;
    -webkit-box-shadow: 0px 10px 13px -7px #000000, 0px 17px 15px 5px rgba(114,202,255,0.42); 
    box-shadow: 0px 10px 13px -11px #000000, 0px 17px 15px 5px rgba(114,202,255,0.35);
    
}
```
![image'](https://github.com/CreativeDave/Tech-Academy-Live-Project/blob/master/media/Screenshot%20from%202019-04-05%2012-04-18.png)

'Auto-post' contains the divs 'rcol' and 'lcol' to display the date and title. I did not use an inline block, instead I specifically gave them their own columns. 
```
.lcol {
    grid-column-start: 1;
    margin-left: 10px;
    font-size: 14px;

}

.rcol {
    grid-column-start: 2; 
    margin-left: 0px;
    padding-top:18px;
    border-radius: 0px 0px 13px 0px;
   

}
```
So, the auto generated rows only contain 2 columns: the 'lcol' for the last-active date, and the 'rcol' for the title and link.

Since base.html already has 'forum-container', and 'main' defined, and there are no sub columns to worry about here, the code is pretty straight-forward. I did add a nice little frame around the container, and a box shadow for each new post. I put the Tech Academy logo up there with a nice little underline as well. 
