from scorer.scorer import matchScorer, htmlTableGenerator
import web

urls = (
  '/hello', 'Index'
)
app = web.application(urls, globals())
render = web.template.render('templates/')

class Index(object):
	def GET(self):
		return render.hello_form()

	def POST(self):
		form = web.input(greet="Hello")
		lyric_text = "%s" %form.lyric_text
		no_of_res = "%s" %form.no_of_matches
		matches = matchScorer().getTopnMatches(lyric_text, no_of_res)
		with open("templates/out.html",'wb') as fid:
			fid.write(htmlTableGenerator().generateTable(matches))
		# print htmlTableGenerator().generateTable(matches)
		# return render.index(greeting = lyric_text)
		return render.out("makerender")

if __name__ == '__main__':
	app.run()