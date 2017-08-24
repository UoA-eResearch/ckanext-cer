import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class CerPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cer')

    def before_search(self, search_params):
        fq = search_params.get('fq', '')
        fq += ' -child_of:[* TO *]'
        search_params['fq'] = fq
        
        return search_params
