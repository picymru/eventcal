% include('global/header.tpl')
<section class="hero">
	<div class="container">
			<h1>Events</h1>
	</div>
</section>

<section id="content" class="content">
	<div class="container">
		<div class="onecolumn">
			% for event in events:
			<div class="event">
				<h2>{{event['title']}}</h2>
				<div class="blog-item">
					<h6 class="date"><span class="icon-calendar"></span>
					{{event['date']}}
					
					% if event['time'] != "00:00" and event['timeEnd'] != "00:00":
					 {{event['time']}}
					% elif event['date'] != event['dateEnd']:
					 - {{event['dateEnd']}}
					% end

					% if event['time'] != event['timeEnd']:
					 - {{event['timeEnd']}}
					% end
					</h6>
					{{!event['desc'].split('<!--more-->')[0] or "<br />"}}
					<a class="read-more" href="/event/{{event['id']}}">View event page &raquo;</a>
				</div>
			</div>
			% end
		</div>
	</div>
% include('global/footer.tpl')