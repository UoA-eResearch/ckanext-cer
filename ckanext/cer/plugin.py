import logging
import ckan.logic as logic
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.uploader as uploader
try:
    import astropy.io.fits as fits
except ImportError:
    import pyfits as fits

import wand.image as image
import routes.mapper as mapper
import ckan.controllers.organization as organization

log = logging.getLogger(__name__)
get_action = logic.get_action

class CerPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    #plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cer')

    def before_search(self, search_params):
        fq = search_params.get('fq', '')
        fq += ' -child_of:[* TO *]'
        search_params['fq'] = fq
        return search_params

    def before_map(self, map):
        map.redirect('/organization', '/project',
                 _redirect_code='301 Moved Permanently')
        map.redirect('/organization/{url:.*}', '/project/{url}',
                 _redirect_code='301 Moved Permanently')

#        org_controller = organization.OrganizationController

        with mapper.SubMapper(map, controller= 'organization') as m:
            m.connect('project_index', '/project', action='index')
            m.connect('/project/list', action='list')
            m.connect('/project/new', action='new')
            m.connect('/project/{action}/{id}',
                      requirements=dict(action='|'.join([
                          'delete',
                          'admins',
                          'member_new',
                          'member_delete',
                          'history'
                      ])))
            m.connect('project_activity', '/project/activity/{id}/{offset}',
                      action='activity', ckan_icon='clock-o')
            m.connect('project_read', '/project/{id}', action='read')
            m.connect('project_about', '/project/about/{id}',
                      action='about', ckan_icon='info-circle')
            m.connect('project_read', '/project/{id}', action='read',
                      ckan_icon='sitemap')
            m.connect('project_edit', '/project/edit/{id}',
                      action='edit', ckan_icon='pencil-square-o')
            m.connect('project_members', '/project/members/{id}',
                      action='members', ckan_icon='users')
            m.connect('project_bulk_process',
                      '/project/bulk_process/{id}',
                      action='bulk_process', ckan_icon='sitemap')


        return map


  #  def after_create(self, context, resource):
  #      log.debug(context)        
  #      pkg = get_action('package_show')(context, {'id':resource['package_id']})
  #      log.debug(pkg)
  #      if resource.get('url_type') == 'upload':
  #          upload = uploader.get_resource_uploader(resource)
  #          filepath = upload.get_path(resource['id'])
  #      
  #      additional_metadata = self.get_metadata(filepath)
  #      for n, p in enumerate(pkg['resources']):
  #          if p.get('id') == resource['id']:
  #              break
  #      else:
  #          n = -1
  #          pkg['resources'][n]['id'] = resource['id']

  #      pkg['resources'][n].update(additional_metadata)
  #      pkg['resources'][n]['format'] = 'fits'
  #      log.debug(pkg)
  #      context['model'].repo.session.rollback()
  #      context['defer_commit'] = True        
  #      get_action('package_update')(context, pkg)
  #      context.pop('defer_commit')

  #  def get_metadata(self, file_path):
  #      hdulist = fits.open(file_path, memmap=True)
  #      header = hdulist[0].header

  #      #fits_keywords = ('SIMPLE', 'BITPIX', 'NAXIS')
  #      #metadata = [dict((keyword, header[keyword]) 
  #      #    for keyword in fits_keywords)]

  #      res_meta = {}
  #      for k, v in header.items():
  #          if k != '':
  #              res_meta[k] = v

  #      hdulist.close()
  #      return res_meta
