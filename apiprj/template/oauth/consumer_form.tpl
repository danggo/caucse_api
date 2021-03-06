{%extends "base.tpl"%}

{% block breadcrumbs %}
	<div class="breadcrumbs">
		<a href="/">홈</a> &rsaquo; 
		<a href="/accounts/profile">내 애플리케이션 관리</a> &rsaquo; 
		새 애플리케이션 등록
	</div>
{% endblock %}

{% block content %}
	<h1>새 애플리케이션 등록</h1>
	<fieldset class="module aligned "> 
	<h2>새 애플리케이션</h2>
	<form method="post">
		{%csrf_token%}
		<table> 
		{{ form.as_table }}
		</table>
		<p>
		    <input type='submit' value='등록'/><input type='hidden' name='oauth_token' value='{{ oauth_token }}'/>
		</p>
	</form>
	</fieldset>
{% endblock %} 