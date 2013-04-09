import pytest
import jinja2
from formfill import FormFillExtension


@pytest.fixture
def jinja_env():
    env = jinja2.Environment(extensions=[FormFillExtension])
    return env


def test_formfill(jinja_env):
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


def test_formfill_without_errors(jinja_env):
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


def test_formfill_without_args(jinja_env):
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


def test_formfill_with_wrong_args(jinja_env):
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
