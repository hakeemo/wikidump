import mako.runtime
import mako.template

pages_revisions_template = '''
<root>
    % for page in pages:
    <page>
        <title>${page.title}</title>
        <id>${page.id}</id>
        <revisions>
            % for revision in page.revisions:
            <revision>
                <id>${revision.id}</id>
                <timestamp>${revision.timestamp}</timestamp>
                <references_diff>
                    %for diff in revision.references_diff:
                    <diff action="${diff.action}">${diff.data}</diff>
                    %endfor
                </references_diff>
                <publication_identifiers_diff>
                    % for diff in revision.publication_identifiers_diff:
                    <diff action="${diff.action}">\
<%                      identifier = diff.data %>
                        <identifier type="${identifier.type}" id="${identifier.id}" />
                    </diff>
                    % endfor
                </publication_identifiers_diff>
                <sections>
                    %for section in revision.sections:
                    <section level="${section.level}">${section.name}</section>
                    %endfor
                </sections>
                <bibliography>${revision.bibliography}</bibliography>
            </revision>
            %endfor
        </revisions>
    </page>
    % endfor
</root>
'''

stats_template = '''
<stats>
    <performance>
        <start_time>${stats['performance']['start_time']}</start_time>
        <end_time>${stats['performance']['end_time']}</start_time>
        <revisions_analyzed>${stats['performance']['revisions_analyzed']}</revisions_analyzed>
        <pages_analyzed>${stats['performance']['pages_analyzed']}</pages_analyzed>
    </performance>
    <identifiers>
        % for where, count in stats['identifiers'].items():
        <appearance where="${where}" count="${count}" />
        % endfor
    </identifiers>
</stats>
'''

_default_filters = [
    'str',   # Unicode
    'x',     # XML
]


def _render_xml_template(template, output_handler, **kwargs):
    ctx = mako.runtime.Context(output_handler, **kwargs)

    xml_template = mako.template.Template(
        template,
        default_filters=_default_filters,
    )
    xml_template.render_context(ctx)


def serialize_page_revisions(pages, output_handler):
    _render_xml_template(pages_revisions_template, output_handler, pages=pages)


def serialize_stats(stats, output_handler):
    _render_xml_template(stats_template, output_handler, stats=stats)
