{%extends "base.tpl"%}

{% block title %}
	동네API - 상태
{% endblock %}

{% block content %}
	<h1>My Consumers</h1>
	{% for consumer,token in consumer_token %}
	<h2>{{ consumer.name|escape }}</h2>
	<ul>
	    <li>
	        관리자: {{consumer.user_id}}
	    </li>
	    <li>
	        생성일: {{consumer.created|timesince}} 전
	    </li>
	    <li>
	        설명: {{consumer.description|escape}}
	    </li>
	    <li>
	        consumer key: {{consumer.key|escape}}
	    </li>
	    <li>
	        consumer secret: {{consumer.secret|escape}}
	    </li>
	    {% if token %}
		    <li>
		        access token key: {{token.key}}
		    </li>
		    <li>
		        access token key: {{token.secret}}
		    </li>
	    {% endif %}
	</ul>
	{% endfor %}
{%endblock%}