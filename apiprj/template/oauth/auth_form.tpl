{%extends "base.tpl"%}

{% block content %}
	<h1>{{ consumer.name }} 애플리케이션이 동문님의 동문 네트워크 서비스 계정으로의 접근을 요청하고 있습니다.</h1>
	<p>
	    {{ consumer.user_id }} 동문이 작성한 {{ consumer.name }} 애플리케이션이 
	    동문님의 동문 네트워크 데이터를 사용하도록 허용하시겠습니까? 
	</p>
	
	<form method="post" action="/oauth/authorize">
		{%csrf_token%} 
		{% if user.is_authenticated %}
		    <p>
		        {{ user.username }}님이 아니신 경우                             
				{% if oauth_token %}
					<a href='/accounts/logout?next=/oauth/authorize?oauth_token={{oauth_token}}'>로그아웃</a>
		        {% else %}
		        	<a href='/accounts/logout_then_login'>로그아웃</a>
		        {% endif %}
				후 이용해 주세요.
		    </p>
		{% else %}
		    <p>
		        {{ message }}
		    </p>
		    <p>
		        아이디: <input name='user_id'/>
		    </p>
		    <p>
		        비밀 번호: <input name='password' type='password'/>
		    </p>
		{% endif %}
		<p>
		    <input type='submit' value='Allow'/><input type='hidden' name='oauth_token' value='{{ oauth_token }}'/>
		</p>
	</form>
{% endblock %} 