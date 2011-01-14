<!doctype HTML>
<html>
    <head>
        <title>
        	{%block title%}
        		동네API
    		{%endblock%}
        </title>
        <meta content='text/html; charset=UTF-8'>
        <link rel="stylesheet" type="text/css" href="/api_static/css/caucse_api.css" />
    </head>
    <body>
        <div id='container'>
            <div id='header'>
                <div id='logo'>
                    <a href='/'><img src='http://www.caucse.net/page/images/home_menu_logo.gif'></a>
                </div>
                <div id='nav'>
                    <ul class='nav'>
                    
                        {% block navibar %} 
	                        <li class='nav'>
	                            <a href='/apistatus'>시스템 상태</a>
	                        </li>
	                        <li class='nav'>
	                            <a href='/apireference'>API 레퍼런스</a>
	                        </li>
	                        {% if user.is_authenticated %}
		                        <li class='nav'>
		                            <a href='/accounts/profile'>내 애플리케이션</a>
		                        </li>
		                        <li class='nav'>
		                            {% if oauth_token %}
		                            	<a href='/accounts/logout?next=/oauth/authorize?oauth_token={{oauth_token}}'>logout</a>
		                            {% else %}
		                            	<a href='/accounts/logout_then_login'>로그아웃</a>
		                            {% endif %}
		                        </li>
	                        {% else %}
		                        <li class='nav'>
		                            <a href='/accounts/login'>로그인</a>
		                        </li>
	                        {% endif %}
                        {% endblock %}
                        
                    </ul>
                </div>
            </div>
            <div id='content'>
            
                {% block content %} 
                	내용! 
            	{%endblock%}
            	
            </div>
            <div id='footer'>
                <p>
                    문의: 이덕준 (<a href='mailto:gochist@gmail.com'>gochist@gmail.com</a>)
                </p>
            </div>
        </div>
    </body>
</html>
