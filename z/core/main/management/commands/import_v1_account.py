# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from z.saas.models import Account
from z.core.logo.models import Logo
from z.meta.option.models import Option
from z.meta.idtag.models import IdTag
from z.core.app.models import App, AppRegistration
from z.org.entity.models import Entity, Unit, Activity
from z.org.hr.models import Position#, PositionGroup, PositionExposition
from z.auth.zuser.models import ZUser
from z.auth.acl.models import EntityACL
from z.prev.domain.models import Sector, Domain, SectorRegistration, DomainRegistration
from z.prev.hazard.models import Hazard
from z.prev.action.models import Action, ActionType
from z.prev.profile.models import Profile, ProfileHazard
import z.prev.profile.models as profmodel
from z.prev.assess.v1.models import V1RiskAssessment
from z.prev.assess.v1.models import V1ActionTrack
from z.means.equipment.models import Equipment
from z.prev.activity.models import PrevActivityExt
from z.core import zutils
from optparse import make_option
from z.utils.spiff import db
from django.conf import settings
#import settings
import os
import sys
import os.path

DELETED_SECTOR_NAME = "[deleted sector]"
DELETED_DOMAIN_NAME = "[deleted domain]"

#
# ACL CONF FROM GENERISQUE V1 BACKEND
#
acl_target_uids = {
    # Company structure
    "company":  1,
    "unit":     2,
    "activity": 3,

    # Dangers & actions database
    "sector":                   100,
    "sector_contents":          101,
    "domain":                   110,
    "danger":                   120,
    "action":                   130,
    "profile":                  140
}

# Unix : 1=x 2=w 4=r
# delete :                  1
# modify :                  2
# delete + modify :         3
# read :                    4
# read + delete :           5
# read + modify :           6
# read + modify + delete :  7
action_uids = {
    "delete":           1,
    "del":              1,
    "modify":           2,
    "mod":              2,
    "delete-modify":    3,
    "delmod":           3,
    "read":             4,
    "r":                4,
    "read-modify":      6,
    "rw":               6
}
# 
# 
# 

class Command(BaseCommand):
    help = u'Import customers and module registrations from Générisque V1 sqlite3 database.'

    def add_arguments(self, parser):
        parser.add_argument('account_login', nargs='?', type=str)

    def handle(self, *args, **options):
        print ("--------------------------------")
        print ("* IMPORTING GENERISQUE V1 DATA *")
        print ("--------------------------------")
        if options['account_login'] is not None:
            account_login = options['account_login']
        else:
            print ("!! Account login required !!")
            print (" -> please specify a login for the account to import")
            print ("")
            sys.exit(1)
        print ("- Account : %s" %(account_login))
        admin_db_filename = settings.GENERISQUE_V1_DATAPATH+'/admin_data/customer_base.db'
        account_db_filename = ""
        print ("admin_db_filename : %s" %(admin_db_filename))
        self.admin_db = db.dbms_factory({'type': 'sqlite', 'filename': admin_db_filename})
        print ("admin_db : %s" %(repr(self.admin_db)))
#        sys.exit(0)
        account_db_filename = "%s/customers_data/%s/%s.db" %(settings.GENERISQUE_V1_DATAPATH, account_login, account_login)
        gv1account = self.admin_db.query_dict("SELECT * FROM Customer WHERE login='"+account_login+"'")[0]
        if os.path.isfile(account_db_filename):
            try:
                self.db = db.dbms_factory({'type': 'sqlite', 'filename': account_db_filename})
            except:
                print("!! Error opening sqlite3 database file : %s" %(account_db_filename))
                sys.exit(1)
            a, created = Account.objects.get_or_create(login=account_login)
            a.name = gv1account['name']
            a.save()

            # Todo : set admin user

            # Logo
            logo_filename = "%s/customers_data/%s/files/logo.png" %(settings.GENERISQUE_V1_DATAPATH, account_login)
            if os.path.exists(logo_filename):
                import shutil
                new_filename = "%s/logos/logo_%s.png" %(a.login, a.login)
                print (" - Logo file exists, copying into '%s'" %(new_filename))
                shutil.copy(logo_filename, os.path.join(settings.ACCOUNT_DATA_ROOT, new_filename))
                l = Logo(account=a, title="logo %s" %(a.name))
                l.image = os.path.join(settings.ACCOUNT_DATA_ROOT, new_filename)
                l.save()
                a.logo = l
                a.save()
            else:
                print (" - Logo file not found, skipping logo")







            #
            # Import all INVARIANT from customer database.
            #
            
            # Equipments
            equipment_list = self.db.query_dict("SELECT * FROM PROF__Equipment")
            equipment_index = {}
            for equipment in equipment_list:
                # search for selected equipments to narrow the import list
                eq_count = self.db.query_dict("SELECT COUNT(*) AS nb FROM PROF__EquipmentActivity WHERE equipment_id="+str(equipment['equipment_id']))[0]['nb']
                if int(eq_count) > 0:
                    eq = Equipment(account=a, name=equipment['name'], type=int(equipment['type']))
                    eq.save()
                    equipment_index[equipment['equipment_id']] = eq.id
                    i = IdTag(content_object=eq, value=equipment['equipment_id'])
                    i.save()
            print ("    %d equipment(s) imported" %(len(equipment_index)))

            # Action types
            action_type_list = self.db.query_dict('SELECT * FROM PROF__ActionType')
            action_type_index = {}
            for action_type in action_type_list:
                at, created = ActionType.objects.get_or_create(account=a, name=action_type['name'])
                if created:
                    at.save()
                    i = IdTag(content_object=at, value=action_type['action_type_id'])
                    i.save()
                action_type_index[action_type['action_type_id']] = at.id
            print ("    %d action type(s) imported" %(len(action_type_index)))








            # PROFILES
            #profile_list = self.db2.query_dict("SELECT * FROM PROF__Profile")
            # Import only profiles in use
            profile_list = self.db.query_dict("SELECT DISTINCT p.* FROM PROF__Profile p, MAIN__Activity a where a.profile_id=p.profile_id")
            profile_index = {}
            for profile in profile_list:
                p = Profile(account=a, 
                        type=profmodel.Z_PREV_PROFILETYPE_HAZARD, name=profile['name'])
#                p.name = profile['name']
                p.save()
                profile_index[profile['profile_id']] = p.id
                i = IdTag(content_object=p, value=profile['profile_id'])
                i.save()
#                hazard_list_in_profile = self.db.query_dict("SELECT * FROM PROF__ProfileDanger WHERE profile_id="+str(profile['profile_id']))
#                for hip in hazard_list_in_profile:
#                    ha = None
#                    if hip['danger_id'] in hazard_index.keys():
#                        ha = Hazard.objects.get(id=hazard_index[hip['danger_id']])
#                    if ha is not None:
#                        ph = ProfileHazard(profile=p, hazard=ha)
#                        ph.save()
            print ("    %d profile(s) imported" %(len(profile_index)))


            print ("  - Invariant imported, proceeding with entities")














            #
            # Import Entities
            # - Entity layout : units & activities
            # - HR-related : positions, expositions
            #
            entity_list = self.db.query_dict("SELECT * FROM MAIN__Company ORDER BY NAME ASC")
            entity_index = {}
            unit_index = {}
            activity_index = {}
            position_index = {}
            entity_count = 0
            for entity in entity_list:
                entity_count += 1
                print ('        - entity %d of %d : %s' %(entity_count, len(entity_list), entity['name']))
                position_names = []
                if str(entity['ref_id']).isdigit():
                    entity['ref_id'] = int(entity['ref_id'])
                else:
                    entity['ref_id'] = 0
                e = Entity( name = entity['name'], account=a)
                if True:


#                    e.account = a
                    if str(entity['ref_active'])!="0":
                        _key_exists = False
                        _key_value = 0
                        if 'ref_id' in entity_index:
                            _key_exists = True
                            _key_value = entity_index[entity['ref_id']]
                            print ('      Entity "%s" has ref #%s activated (%s, %s)' %(entity['name'], repr(entity['ref_id']), repr(_key_exists), repr(_key_value)))
                            eref = Entity.objects.get(id=entity_index[entity['ref_id']])
                            print ('    Ref active for entity "%s", refering to #%d (%s)' %(entity['name'], entity['ref_id'], e.name))
                            e.ref = eref
                            e.ref_active = True
                    e.save()
                    entity_index[entity['company_id']] = e.id
                    i = IdTag(content_object=e, value=entity['company_id'])
                    i.save()
                    # POSITIONS
                    for position_group in self.db.query_dict('SELECT * FROM MAIN__PositionRegroupment WHERE company_id=%d' %(entity['company_id'])):
                        # 
                        # ToDo : create Position Regroupments
                        # 
                        pass
                    for position in self.db.query_dict('SELECT * FROM MAIN__Position WHERE company_id=%d' %(entity['company_id'])):
                        while position['name'] in position_names:
                            position['name'] += '_'
                        position_names.append(position['name'])
                        pos = Position(name=position['name'], entity=e)
#                        pos.entity = e
                        if str(position['employees']).isdigit():
                            pos.people_count = int(position['employees'])
                        pos.save()
                        position_index[position['position_id']] = pos.id
                        i = IdTag(content_object=pos, value=position['position_id'])
                        i.save()

                    # UNITS
                    unit_list = self.db.query_dict('SELECT * FROM MAIN__Unit WHERE company_id='+str(entity['company_id']))
                    for unit in unit_list:
                        _ref_valid = False
                        if str(unit['ref_id']).isdigit():
                            unit['ref_id'] = int(unit['ref_id'])
                            if unit['ref_id'] in unit_index:
                                _ref_valid = True
                        u = Unit(name = unit['name'])
                        u.entity = e
                        if _ref_valid and Unit.objects.filter(id=unit_index[unit['ref_id']]).count()>0:
                            uref = Unit.objects.get(id=unit_index[unit['ref_id']])
                            u.ref = uref
                        u.save()
                        unit_index[unit['unit_id']] = u.id
                        i = IdTag(content_object=u, value=unit['unit_id'])
                        i.save()
                        activity_list = self.db.query_dict('SELECT * FROM MAIN__Activity WHERE unit_id='+str(unit['unit_id']))
                        #ACTIVITES
                        for activity in activity_list:
                            _ref_valid = False
                            if str(activity['ref_id']).isdigit():
                                activity['ref_id'] = int(activity['ref_id'])
                                if activity['ref_id'] in activity_index:
                                    _ref_valid = True
                            else:
                                activity['ref_id'] = 0
                            print ('      - Activity "%s" refering #%d (%s)' %(activity['name'], activity['ref_id'], repr(_ref_valid)))
                            act = Activity(name = activity['name'], entity=e)
#                            a.entity = e
                            act.save()
                            act.unit = u
                            if _ref_valid and Activity.objects.filter(id=activity_index[activity['ref_id']]).count()>0:
                                aref = Activity.objects.get(id=activity_index[activity['ref_id']])
                                act.ref = aref

                            act.set_info("post_type", activity['post_type'])
                            act.set_info("schedule_type", activity['schedule_type'])
                            act.set_info("employment_type", activity['employment_type'])
                            act.set_info("displays", activity['displays'])

                            equipment_list = self.db.query_dict('SELECT * FROM PROF__EquipmentActivity WHERE activity_id='+str(activity['activity_id']))
                            for equipment in equipment_list:
                                eq = Equipment.objects.get(id=equipment_index[equipment['equipment_id']])
                                act.equipments.add(eq)


                            act.save()
                            activity_index[activity['activity_id']] = act.id
                            i = IdTag(  content_object=act,
                                        value=activity['activity_id'])
                            i.save()

                            # ACTIVITY EXTENSION (PROFESSIONNAL RISKS)
                            ae = PrevActivityExt(activity=act)
                            if activity['profile_id'] is not None \
                                    and str(activity['profile_id']).isdigit():
                                profile = Profile.objects.get(id=profile_index[int(activity['profile_id'])])
                                ae.profile = profile
                            ae.save()



        else:
            print("!! Sqlite database file for customer %s not found (%s)" %(account_login, account_db_filename))





























    def toto(self):
        # CREATES GENERISQUE CUSTOMER
        gcust = Customer.objects.get(login="generisque")


        if True:



            # 
            # Adds invariant to MASTER base
            # 
            
            # Sectors & domains

            _deleted_sector, created = Sector.objects.get_or_create(custowner=gcust, name=DELETED_SECTOR_NAME)
            _deleted_domain, created = Domain.objects.get_or_create(custowner=gcust, name=DELETED_DOMAIN_NAME, defaults={'sector': _deleted_sector})

            sector_list = self.db2.query_dict("SELECT * FROM PROF__Sector")
            sector_index = {}
            domain_index = {}
            master_sector_index = {}
            master_domain_index = {}
            for sector in sector_list:
                s, created = Sector.objects.get_or_create(custowner=gcust, name=sector['name'])
                if created:
                    s.save()
                    id = IdTag(content_object=s, value=sector['sector_id'])
                    id.save()
                master_sector_index[sector['sector_id']] = s.id
                domain_list = self.db2.query_dict("SELECT * FROM PROF__Domain WHERE sector_id="+str(sector['sector_id']))
                for domain in domain_list:
                    dom, created = Domain.objects.get_or_create(custowner=gcust, name=domain['name'], defaults={'sector': s})
                    if created:
                        dom.save()
                        id = IdTag(content_object=dom, value=domain['domain_id'])
                        id.save()
                    master_domain_index[domain['domain_id']] = dom.id
            sector_index = master_sector_index
            domain_index = master_domain_index

            # Hazards & Actions
            hazard_list = self.db2.query_dict("SELECT * FROM PROF__Danger")
            hazard_index = {}
            master_hazard_index = {}
            for hazard in hazard_list:
                if hazard['domain_id'] in domain_index.keys():
                    dom = Domain.objects.get(id=domain_index[hazard['domain_id']])
                else:
                    dom = _deleted_domain
                if hazard['comment'] is None:
                    hazard['comment'] = ""  
                if not str(hazard['danger_level']).isdigit():
                    hazard['danger_level']=1
                ha, created = Hazard.objects.get_or_create(custowner=gcust, domain=dom, cause=hazard['cause'], consequence=hazard['consequence'])
                if created:
                    ha.level = int(hazard['danger_level'])
                    ha.comment = hazard['comment']
                    ha.save()
                    id = IdTag(content_object=ha, value=hazard['danger_id'])
                    id.save()
                master_hazard_index[hazard['danger_id']] = ha.id
            hazard_index = master_hazard_index

            action_list = self.db2.query_dict("SELECT * FROM PROF__Action")
            action_index = {}
            master_action_index = {}
            for action in action_list:
                if action['domain_id'] in domain_index.keys():
                    dom = Domain.objects.get(id=domain_index[action['domain_id']])
                else:
                    dom = _deleted_domain
                at = None
                if str(action['action_type_id']).isdigit() and str(action['action_type_id'])!="0":
                    if action['action_type_id'] in action_type_index.keys():
                        at = ActionType.objects.get(id=action_type_index[action['action_type_id']])
                if action['comment'] is None or action['comment']=="_":
                    action['comment'] = ""
                if action['consequence'] is None or action['consequence']=="_":
                    action['consequence'] = ""
                act, created = Action.objects.get_or_create(custowner=gcust, domain=dom, caption_todo=action['caption_todo'])
                if created:
                    if at:
                        act.type = at
                    act.caption_done = action['caption_done']
                    act.hazard_consequence = action['consequence']
                    act.comment = action['comment']
                    act.save()
                    id = IdTag(content_object=act, value=action['action_id'])
                    id.save()
                master_action_index[action['action_id']] = act.id
            action_index = master_action_index


            # 
            # Detect which Sector/Domains are effectively used
            # 
            # - loop through profiles associated to activities
            # - add domains with danger(s) selected in profile to domain_list
            #   - add related sector to sector_list 
            # 

            sector_registrations = []
            domain_registrations = []
            print ("    scanning database to find used sectors/domains")          
            query = 'SELECT DISTINCT d.domain_id, d.name as domain_name, s.sector_id, s.name as sector_name '
            query += 'FROM PROF__Domain d, PROF__Sector s, PROF__ProfileDanger pd, PROF__Danger da '
            query += 'WHERE s.sector_id=d.sector_id AND d.domain_id=da.domain_id AND da.danger_id=pd.danger_id AND '
            query += 'pd.profile_id IN '
            query += '(SELECT DISTINCT p.profile_id FROM PROF__Profile p, MAIN__Activity a WHERE p.profile_id=a.profile_id)'
            sect_dom_list = self.db2.query_dict(query)
            for sect_dom in sect_dom_list:
                if not sect_dom['sector_id'] in sector_index:
                    s = Sector(custowner=c, name=sect_dom['sector_name'])
                    s.save()
                    sector_index[sect_dom['sector_id']] = s.id
                    id = IdTag(content_object=s, value=sect_dom['sector_id'])
                    id.save()
                else:
                    s = Sector.objects.get(id=sector_index[sect_dom['sector_id']])
                if not sect_dom['domain_id'] in domain_index:
                    d = Domain(custowner=c, name=sect_dom['domain_name'])
                    d.sector = s
                    d.save()
                    domain_index[sect_dom['domain_id']] = d.id
                    id = IdTag(content_object=d, value=sect_dom['domain_id'])
                    id.save()
                else:
                    d = Domain.objects.get(id=domain_index[sect_dom['domain_id']])
                if s.id not in sector_registrations:
                    sr = SectorRegistration(customer=c, sector=s)
                    sr.save()
                if d.id not in domain_registrations:
                    dr = DomainRegistration(customer=c, domain=d)
                    dr.save()


                    # Hazards & Actions
                    hazard_list = self.db2.query_dict("SELECT * FROM PROF__Danger WHERE domain_id="+str(sect_dom['domain_id']))
                    for hazard in hazard_list:
                        if hazard['danger_id'] not in hazard_index:
                            if hazard['domain_id'] in domain_index.keys():
                                dom = Domain.objects.get(id=domain_index[hazard['domain_id']])
                            else:
                                dom = _deleted_domain
                            if hazard['comment'] is None:
                                hazard['comment'] = ""
                            if not str(hazard['danger_level']).isdigit():
                                hazard['danger_level']=1
                            ha = Hazard(domain=d)
                            ha.custowner = c
                            ha.cause = hazard['cause']
                            ha.consequence = hazard['consequence']
                            ha.level = int(hazard['danger_level'])
                            ha.comment = hazard['comment']
                            ha.save()
                            hazard_index[hazard['danger_id']] = ha.id
                            id = IdTag(content_object=ha, value=hazard['danger_id'])
                            id.save()

                    action_list = self.db2.query_dict("SELECT * FROM PROF__Action WHERE domain_id="+str(sect_dom['domain_id']))
                    for action in action_list:
                        if action['action_id'] not in action_index:
                            if action['domain_id'] in domain_index.keys():
                                dom = Domain.objects.get(id=domain_index[action['domain_id']])
                            else:
                                dom = _deleted_domain
                            at = None
                            if str(action['action_type_id']).isdigit() and str(action['action_type_id'])!="0":
                                if action['action_type_id'] in action_type_index.keys():
                                    at = ActionType.objects.get(id=action_type_index[action['action_type_id']])
                            if action['comment'] is None:
                                action['comment'] = ""
                            if action['consequence'] is None:
                                action['consequence'] = ""
                            act = Action(domain=d)
                            act.custowner = c
                            if at:
                                act.type = at
                            act.caption_todo = action['caption_todo']
                            act.caption_done = action['caption_done']
                            act.hazard_consequence = action['consequence']
                            act.comment = action['comment']
                            act.save()
                            action_index[action['action_id']] = act.id
                            id = IdTag(content_object=act, value=action['action_id'])
                            id.save()
            # 
            # re-check if all dangers and actions used by cotations have been created
            # (some dangers may be coted but not selected in profiles)
            risk_list = self.db2.query_dict('SELECT * FROM PROF__DangerEvaluation')
            for risk in risk_list:
                if not risk['danger_id'] in hazard_index:
                    hazard = self.db2.query_dict('SELECT * FROM PROF__Danger WHERE danger_id='+str(risk['danger_id']))[0]
                    if not hazard['domain_id'] in domain_index.keys():
                        sect_dom = self.db2.query_dict('SELECT d.domain_id, d.name AS domain_name, s.sector_id, s.name AS sector_name FROM PROF__Domain d, PROF__Sector s WHERE d.sector_id=s.sector_id AND d.domain_id='+str(hazard['domain_id']))[0]
                        if not sect_dom['sector_id'] in sector_index:
                            s = Sector(custowner=c, name=sect_dom['sector_name'])
                            s.save()
                            sector_index[sect_dom['sector_id']] = s.id
                            id = IdTag(content_object=s, value=sect_dom['sector_id'])
                            id.save()
                        else:
                            s = Sector.objects.get(id=sector_index[sect_dom['sector_id']])
                        d = Domain(custowner=c, sector=s, name=sect_dom['domain_name'])
                        d.save()
                        domain_index[sect_dom['domain_id']] = d.id
                        id = IdTag(content_object=d, value=sect_dom['domain_id'])
                        id.save()
                    else:
                        d = Domain.objects.get(id=domain_index[sect_dom['domain_id']])
                    if hazard['comment'] is None:
                        hazard['comment'] = ""
                    if not str(hazard['danger_level']).isdigit():
                        hazard['danger_level']=1
                    ha = Hazard(domain=d)
                    ha.custowner = c
                    ha.cause = hazard['cause']
                    ha.consequence = hazard['consequence']
                    ha.level = int(hazard['danger_level'])
                    ha.comment = hazard['comment']
                    ha.save()
                    hazard_index[hazard['danger_id']] = ha.id
                    id = IdTag(content_object=ha, value=hazard['danger_id'])
                    id.save()

            action_cot_list = self.db2.query_dict("SELECT * FROM PROF__Actiontrack")
            for action_cot in action_cot_list:
                if not action_cot['action_id'] in action_index:
                    action = self.db2.query_dict('SELECT * FROM PROF__Action WHERE action_id='+str(action_cot['action_id']))[0]
                    if not action['domain_id'] in domain_index.keys():
                        print ("!!! : %s" %(repr(action)))
                        sect_doms = self.db2.query_dict('SELECT d.domain_id, d.name AS domain_name, s.sector_id, s.name AS sector_name FROM PROF__Domain d, PROF__Sector s WHERE d.sector_id=s.sector_id AND d.domain_id='+str(action['domain_id']))
                        if len(sect_doms)>0:
                            sect_dom  =sect_doms[0]
                        else:
                            sect_dom = {'sector_name': '[deleted sector]', 'sector_id': 0, 'domain_name': '[deleted domain]', 'domain_id': 0}
                        if not sect_dom['sector_id'] in sector_index:
                            s = Sector(custowner=c, name=sect_dom['sector_name'])
                            s.save()
                            sector_index[sect_dom['sector_id']] = s.id
                            id = IdTag(content_object=s, value=sect_dom['sector_id'])
                            id.save()
                        else:
                            s = Sector.objects.get(id=sector_index[sect_dom['sector_id']])
                        d = Domain(custowner=c, sector=s, name=sect_dom['domain_name'])
                        d.save()
                        domain_index[sect_dom['domain_id']] = d.id
                        id = IdTag(content_object=d, value=sect_dom['domain_id'])
                        id.save()
                    else:
                        d = Domain.objects.get(id=domain_index[sect_dom['domain_id']])
                    at = None
                    if str(action['action_type_id']).isdigit() and str(action['action_type_id'])!="0":
                        if action['action_type_id'] in action_type_index.keys():
                            at = ActionType.objects.get(id=action_type_index[action['action_type_id']])
                    if action['comment'] is None:
                        action['comment'] = ""
                    if action['consequence'] is None:
                        action['consequence'] = ""
                    act = Action(domain=d)
                    act.custowner = c
                    if at:
                        act.type = at
                    act.caption_todo = action['caption_todo']
                    act.caption_done = action['caption_done']
                    act.hazard_consequence = action['consequence']
                    act.comment = action['comment']
                    act.save()
                    action_index[action['action_id']] = act.id
                    id = IdTag(content_object=act, value=action['action_id'])
                    id.save()














            if True:
                if True:
                    if True:
                        if True:








#                            return True

                            # RISKS ASSESSMENTS
                            risk_list = self.db2.query_dict('SELECT * FROM PROF__DangerEvaluation WHERE activity_id='+str(activity['activity_id']))
                            for risk in risk_list:
                                hz = Hazard.objects.get(id=hazard_index[risk['danger_id']])
                                r = V1RiskAssessment(activity=a, hazard=hz)
                                r.comment = risk['comment']
                                if str(risk['crit_frequency']) in ['1', '2', '3', '4']:
                                    r.frequency = int(risk['crit_frequency'])
                                if str(risk['crit_individual']).lower() in ['a', 'b', 'c', 'd']:
                                    r.individual_protection = str(risk['crit_individual']).upper()
                                if str(risk['crit_collective']).lower() in ['a', 'b', 'c', 'd']:
                                    r.collective_protection = str(risk['crit_collective']).upper()
                                if str(risk['crit_training']).lower() in ['a', 'b', 'c', 'd']:
                                    r.training = str(risk['crit_training']).upper()
                                if str(risk['crit_information']).lower() in ['a', 'b', 'c', 'd']:
                                    r.information = str(risk['crit_information']).upper()
                                r.save()
                            
                            # ACTION COTATIONS
                            action_list = self.db2.query_dict('SELECT * FROM PROF__ActionTrack WHERE activity_id='+str(activity['activity_id']))
                            for action in action_list:
                                act = Action.objects.get(id=action_index[action['action_id']])
                                at = V1ActionTrack(activity=a, action=act)
                                if str(action['status'])!='0':
                                    at.status=1
                                at.comment = action['comment']
                                at.responsible = action['responsible']
                                at.save()
                            
                            # MATRIX CONTENTS
                            matrix_list = self.db2.query_dict('SELECT * FROM MAIN__Matrix WHERE activity_id='+str(activity['activity_id']))
                            for matrix in matrix_list:
                                if matrix['position_id'] in position_index.keys():
                                    pos = Position.objects.get(id=position_index[matrix['position_id']])
                                    if PositionExposition.objects.filter(activity=a, position=pos).count()==0:
                                        pe = PositionExposition(activity=a,
                                                            position=pos)
                                        pe.value = matrix['value']
                                        pe.save()
            # Importing users
            user_list = self.db2.query_dict('SELECT * FROM MAIN__User')
            user_index = {}
            for user in user_list:
#                u = User(username=gutils.full_username(user['login'], c))
                u, created = User.objects.get_or_create(username=gutils.full_username(user['login'], c))
                if user['email']!="" and user['email'] is not None:
                    u.email = user['email']
                else:
                    u.email = "ch@nge.me"
                u.last_name = user['name']
                u.password = "md5$$" + user['hash_password']
                u.save()
                user_index[user['user_id']] = u.id
                i = IdTag(content_object=u, value=user['user_id'])
                i.save()
                zu, created = ZUser.objects.get_or_create(user=u, account=a)
                zu.position = user['position']
                zu.phone = user['phone']
                zu.save()
            # Importing ACLs

            acl_list = self.db2.query_dict('SELECT * FROM MAIN__Acl WHERE target_type=1')
            acl_index = {}
            for acl in acl_list:
                if acl['targey_id'] in entity_index and acl['user_id'] in user_index:
                    e = Entity.objects.get(id=entity_index[acl['target_id']])
                    u = User.objects.get(id=user_index[acl['user_id']])
                    ea, created = EntityACL.objects.get_or_create(entity=e, user=u)
                    ea.can_view = True
                    if str(acl['action'])=="6":
                        ea.can_modify = True
                    ea.save()
                    print ("Entity ACL set for user %s on entity %s (%s|%s)" %(u.username, e.name, str(ea.can_view), str(ea.can_modify)))

