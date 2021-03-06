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
		(lyric_text, no_of_res, english_check) = ("%s" %form.lyric_text, "%s" %form.no_of_matches, "%s" %form.radio_btn)
		matches = matchScorer().getTopnMatches(lyric_text, no_of_res, english_check)
		if matches == []:
			with open("templates/out.html",'wb') as fid:
				fid.write('''$def with (sometxt)
				$if sometxt:
					<h1>OOPS, something went wrong :(<\h1>
				$else:
					<h1>OOPS, Something went wrong<\h1>''')
			return render.out("emptypage")
		else:
			with open("templates/out.html",'wb') as fid:
				fid.write(htmlTableGenerator().generateTable(matches))
			return render.out("makerender")

if __name__ == '__main__':
	app.run()