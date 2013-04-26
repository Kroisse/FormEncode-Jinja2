import pytest
import jinja2
from formfill import FormFillExtension


@pytest.fixture
def jinja_env():
    env = jinja2.Environment(extensions=[FormFillExtension])
    return env


def test_with_literal_arguments(jinja_env):
    template = u'''
    {% formfill {'username': 'john doe'}
           with {'username': 'Invalid Username'} -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <form:error name="username">
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    expected = u'''
    <form action="account/signin" method="POST">
        <input type="text" name="username" class="error" value="john doe" />
        <span class="error-message">Invalid Username</span>
        <input type="password" name="password" value="" />
    </form>'''
    result = jinja_env.from_string(template).render()
    assert result == expected


def test_with_variables(jinja_env):
    template = u'''
    {% formfill defaults with errors -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <form:error name="username">
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    expected = u'''
    <form action="account/signin" method="POST">
        <input type="text" name="username" class="error" value="john doe" />
        <span class="error-message">Invalid Username</span>
        <input type="password" name="password" value="" />
    </form>'''

    defaults = {'username': 'john doe'}
    errors = {'username': 'Invalid Username'}
    result = jinja_env.from_string(template).render(defaults=defaults,
                                                    errors=errors)
    assert result == expected


def test_with_expr(jinja_env):
    template = u'''
    {% formfill form.defaults
           with form.errors -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <form:error name="username">
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    expected = u'''
    <form action="account/signin" method="POST">
        <input type="text" name="username" class="error" value="john doe" />
        <span class="error-message">Invalid Username</span>
        <input type="password" name="password" value="" />
    </form>'''

    class Form(object):
        defaults = {'username': 'john doe'}
        errors = {'username': 'Invalid Username'}

    form = Form()
    result = jinja_env.from_string(template).render(form=form)
    assert result == expected


def test_without_errors(jinja_env):
    template = u'''
    {% formfill {'username': 'louis'} -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <form:error name="username">
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    expected = u'''
    <form action="account/signin" method="POST">
        <input type="text" name="username" value="louis" />
        
        <input type="password" name="password" value="" />
    </form>'''
    result = jinja_env.from_string(template).render()
    assert result == expected


def test_without_args(jinja_env):
    template = u'''
    {% formfill -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    with pytest.raises(jinja2.TemplateSyntaxError):
        jinja_env.from_string(template).render()
    template2 = u'''
    {% formfill {'username': 'george'} with -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    with pytest.raises(jinja2.TemplateSyntaxError):
        jinja_env.from_string(template2).render()


def test_with_wrong_args(jinja_env):
    template = u'''
    {% formfill 'michile' -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    with pytest.raises(TypeError) as exc:
        jinja_env.from_string(template).render()
    assert "not 'michile'" in str(exc)
    template2 = u'''
    {% formfill {'username': 'austin'} with ['Invalid Username'] -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    with pytest.raises(TypeError) as exc:
        jinja_env.from_string(template2).render()
    assert "not ['Invalid Username']" in str(exc)


def test_configure(jinja_env):
    jinja_env.formfill_config.update(error_class='fail',
                                     auto_insert_errors=False)
    template = u'''
    {% formfill {'username': 'john doe'}
           with {'username': 'Invalid username',
                 'password': 'Required'} -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <form:error name="username">
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    expected = u'''
    <form action="account/signin" method="POST">
        <input type="text" name="username" class="fail" value="john doe" />
        <span class="error-message">Invalid username</span>
        <input type="password" name="password" class="fail" value="" />
    </form>'''
    result = jinja_env.from_string(template).render()
    assert result == expected


def test_configure_formfill_error_formatter(jinja_env):
    def list_error_formatter(error):
        return '<ul class="errors"><li>{0}</li></ul>'.format(error)
    assert 'default' in jinja_env.formfill_error_formatters
    jinja_env.formfill_error_formatters['list'] = list_error_formatter
    template = u'''
    {% formfill {'username': 'robert'}
           with {'username': 'Invalid username'} -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <form:error name="username" format="list">
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    expected = u'''
    <form action="account/signin" method="POST">
        <input type="text" name="username" class="error" value="robert" />
        <ul class="errors"><li>Invalid username</li></ul>
        <input type="password" name="password" value="" />
    </form>'''
    result = jinja_env.from_string(template).render()
    assert result == expected


def test_with_non_ascii_text(jinja_env):
    template = u'''
    {% formfill {'username': '박재상', 'twitter': '@psy_oppa'}
           with {'username': 'Sorry for rocking with 강남스타일'} -%}
    <form action="account/register" method="POST">
        <input type="text" name="username" />
        <form:error name="username">
        <input type="password" name="password" />
        <input type="text" name="twitter" />
    </form>
    {%- endformfill %}'''
    expected = u'''
    <form action="account/register" method="POST">
        <input type="text" name="username" class="error" value="박재상" />
        <span class="error-message">Sorry for rocking with 강남스타일</span>
        <input type="password" name="password" value="" />
        <input type="text" name="twitter" value="@psy_oppa" />
    </form>'''
    result = jinja_env.from_string(template).render()
    assert result == expected


def test_undefined_variables(jinja_env):
    template = u'''
    {% formfill formdata with errors -%}
    <form action="account/signin" method="POST">
        <input type="text" name="username" />
        <form:error name="username">
        <input type="password" name="password" />
    </form>
    {%- endformfill %}'''
    expected = u'''
    <form action="account/signin" method="POST">
        <input type="text" name="username" value="" />
        
        <input type="password" name="password" value="" />
    </form>'''
    result = jinja_env.from_string(template).render()
    assert result == expected
