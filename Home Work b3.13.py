def attrs_to_str(other):
    attrs = ''
    for attr, value in other.attributes.items():
        attrs += (' %s="%s"' % (attr, value))
        attrs = "".join(attrs)
    return attrs


class Tag:
    def __init__(self, tag = '', text='', is_single = False, klass=None, **kwargs):
        self.tag = tag
        self.text = text
        self.klass = klass
        self.is_single = is_single
        self.attributes = dict()

        if klass is not None:
            self.attributes['class'] = self.klass
            self.attributes['class'] = ', '.join(map(''.join, self.attributes['class']))

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def __iadd__(self, other):
        if other.is_single == False:
            self.text += '\n <{tag}{attrs}>{text}<{tag}>'.format(
                tag = other.tag,
                attrs = attrs_to_str(other),
                text = other.text
                )
        else : self.text += '\n <{tag}{attrs}>\n'.format(
                tag = other.tag,
                attrs = attrs_to_str(other),
                text = other.text
                )
        return self

    def __str__(self):
        if self.is_single is False:
            return '\n<{tag}{attrs}>{text}<{tag}>\n'.format(
                tag = self.tag,
                attrs = attrs_to_str(self),
                text = self.text
            )
        else : return '<{tag}{attrs}>'.format(
            tag = self.tag,
            attrs = attrs_to_str(self),
        )

class TopLevelTag(Tag):
    def __iadd__(self, other):
        self.text += str(other)
        ' <{tag} {attrs}>\n  {other}\n<{tag}>\n'.format(
            tag = self.tag ,
            attrs = self.attributes,
            other = other,
        )
        return self
class HTML:
    def __init__(self, output,**kwargs):
        self.output = output
        self.tag = 'html'
        self.text = ''

    def __iadd__(self, other):
        self.text += str(other)
        return self
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.output, 'w', encoding= 'utf-8') as fp:
            fp.write('<{tag}>\n {other}\n<{tag}>'.format(
                tag = self.tag,
                other = self.text
            ))
        return print('<{tag}>\n {other}\n<{tag}>\n'.format(
            tag=self.tag,
            other=self.text,
        ))

if __name__ == "__main__":
    with HTML(output='test.html') as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body