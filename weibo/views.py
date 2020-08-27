import datetime
from math import ceil

from flask import Blueprint
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from flask import abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from libs.orm import db
from libs.utils import login_required
from weibo.models import Weibo
from weibo.models import Comment
from weibo.models import Like

weibo_bp = Blueprint('weibo', __name__, url_prefix='/weibo', template_folder='./templates')


@weibo_bp.route('/index')
def index():
    '''微博首页'''
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = per_page * (page - 1)
    wb_list = Weibo.query.order_by(Weibo.updated.desc()).limit(per_page).offset(offset)

    max_page = ceil(Weibo.query.count() / per_page)  # 最大页码

    if page <= 3:
        start, end = 1, min(7, max_page)  # 起始处的页码范围
    elif page > (max_page - 3):
        start, end = max_page - 6, max_page  # 结尾处的页码范围
    else:
        start, end = (page - 3), (page + 3)

    pages = range(start, end + 1)
    return render_template('index.html', wb_list=wb_list, pages=pages, page=page)


@weibo_bp.route('/post', methods=("POST", "GET"))
@login_required
def post_weibo():
    '''发布微博'''
    if request.method == "POST":
        uid = session['uid']
        content = request.form.get('content', '').strip()
        now = datetime.datetime.now()

        # 检查微博内容是否为空
        if not content:
            return render_template('post.html', err='微博内容不允许为空')

        weibo = Weibo(uid=uid, content=content, created=now, updated=now)
        db.session.add(weibo)
        db.session.commit()

        return redirect('/weibo/read?wid=%s' % weibo.id)
    else:
        return render_template('post.html')


@weibo_bp.route('/read')
def read_weibo():
    '''阅读微博'''
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)

    # 获取当前微博所有的评论
    comments = Comment.query.filter_by(wid=wid).order_by(Comment.created.desc())
    return render_template('read.html', weibo=weibo, comments=comments)


@weibo_bp.route('/edit', methods=("POST", "GET"))
@login_required
def edit_weibo():
    '''修改微博'''
    # 检查是否是在修改自己的微博
    if request.method == 'POST':
        wid = int(request.form.get('wid', 0))
    else:
        wid = int(request.args.get('wid', 0))
    weibo = Weibo.query.get(wid)
    if weibo.uid != session['uid']:
        abort(403)

    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        now = datetime.datetime.now()

        # 检查微博内容是否为空
        if not content:
            return render_template('edit.html', weibo=weibo, err='微博内容不允许为空')

        # 更新微博内容
        weibo.content = content
        weibo.updated = now
        db.session.commit()

        return redirect(f'/weibo/read?wid={wid}')
    else:
        # 获取微博，并传到模板中
        weibo = Weibo.query.get(wid)
        return render_template('edit.html', weibo=weibo)


@weibo_bp.route('/delete')
@login_required
def delete_weibo():
    '''删除微博'''
    wid = int(request.args.get('wid'))
    # 检查是否是在删除自己的微博
    weibo = Weibo.query.get(wid)

    if weibo.uid == session['uid']:
        db.session.delete(weibo)
        db.session.commit()
        return redirect('/')
    else:
        abort(403)


@weibo_bp.route('/post_comment', methods=("POST",))
@login_required
def post_comment():
    '''发表评论'''
    wid = int(request.form.get('wid'))
    content = request.form.get('content')
    now = datetime.datetime.now()

    # 创建 comment 对象
    comment = Comment(uid=session['uid'], wid=wid, content=content, created=now)
    db.session.add(comment)
    db.session.commit()

    return redirect(f'/weibo/read?wid={wid}')


@weibo_bp.route('/reply', methods=("POST",))
@login_required
def reply():
    '''发表回复'''
    wid = int(request.form.get('wid'))
    cid = int(request.form.get('cid'))
    content = request.form.get('content')
    now = datetime.datetime.now()

    # 创建 comment 对象
    comment = Comment(uid=session['uid'], wid=wid, cid=cid, content=content, created=now)
    db.session.add(comment)
    db.session.commit()

    return redirect(f'/weibo/read?wid={wid}')


@weibo_bp.route('/delete_comment')
def delete_comment():
    cid = int(request.args.get('cid'))
    cmt = Comment.query.get(cid)

    # 检查是否是在删除别人的评论
    if cmt.uid != session['uid']:
        abort(403)

    # 修改数据
    cmt.content = '当前评论已被删除'
    db.session.commit()

    return redirect('/')


@weibo_bp.route('/like')
@login_required
def like():
    uid = session['uid']
    wid = int(request.args.get('wid'))

    lk = Like(uid=uid, wid=wid)
    db.session.add(lk)
    try:
        Weibo.query.filter_by(id=wid).update({'n_like': Weibo.n_like + 1})
        db.session.commit()
    except (FlushError, IntegrityError):
        db.session.rollback()
        Like.query.filter_by(uid=uid, wid=wid).delete()
        Weibo.query.filter_by(id=wid).update({'n_like': Weibo.n_like - 1})
        db.session.commit()

