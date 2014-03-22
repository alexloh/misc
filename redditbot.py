# -*- coding: utf-8 -*- 
import praw
import sys
import unicodecsv
import textwrap
import time

submission_attrs = [
    'created_utc',
    'score',
    'domain',
    'id',
    'title',
    'author',
    'ups',
    'downs',
    'num_comments',
    'permalink',
    'selftext',
    'link_flair_text',
    'over_18',
    'thumbnail',
    'subreddit_id',
    'edited',
    'link_flair_css_class',
    'author_flair_css_class',
    'is_self',
    'name',
    'url',
    'distinguished'
]

NUM_OF_POSTS = 5

if len(sys.argv) < 2:
    exit("Syntax: %s <subreddit>" % sys.argv[0])

subreddit_slug = sys.argv[1].replace('/r/', '')

r = praw.Reddit(user_agent="editer63_diss")

subreddit = r.get_subreddit(subreddit_slug)

print "Scraping %s" % subreddit
with open('%s.csv' % subreddit, 'wb') as csvfile:
    writer = unicodecsv.DictWriter(csvfile, submission_attrs)
    writer.writeheader()
    for link in subreddit.get_top_from_all(limit=NUM_OF_POSTS):
        d = {attr: getattr(link, attr) for attr in submission_attrs}
        d['created_utc'] = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(d['created_utc']))
        writer.writerow(d)
print ("Completed scraping %s" % subreddit)

def showCommentTree(forest, f, level=0):
  for comment in forest:
    f.write(('   '*level)+"------------\n")
    if hasattr(comment, 'body'):
      f.write(('   '*level)+"id: %s\n" % comment.id)
      f.write(('   '*level)+"score: %s\n" % comment.score)
      f.write(('   '*level)+"author: %s\n" % comment.author)
      f.write(textwrap.fill(comment.body.encode('utf-8'), width=70, initial_indent="   "*level, subsequent_indent="   "*level))
      f.write("\n")
      showCommentTree(comment.replies, f, level+1)


for link in subreddit.get_top_from_all(limit=NUM_OF_POSTS):
  pid=getattr(link, 'id')
  f = open('comments_%s.txt' % pid,'w')
  submission = r.get_submission(submission_id=pid)
  forest_comments = submission.comments
  showCommentTree(forest_comments, f, 0)
  f.close()
  t_comments = praw.helpers.flatten_tree(submission.comments)
  with open('comments_%s_result.csv' % pid, 'wb') as csvfile:
    writer = unicodecsv.DictWriter(csvfile, ['id', 'score', 'author'])
    writer.writeheader()
    for comment in t_comments:
      if hasattr(comment, 'body'):
        d = {'id': comment.id, 'score': comment.score, 'author': comment.author }
        writer.writerow(d)


