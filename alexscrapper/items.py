# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AlexscrapperItem(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()
	sid 		= scrapy.Field()
	ctype 		= scrapy.Field()

# activityjunky.com
class ActiveJunky(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()
		
#couponcactus.com
class CouponCactus(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()

#couponcactus.com
class Befrugal(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()

#bonuscashcenter.citicards.com
class BonusCashCenter(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()

#discover.com
class Discover(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()

class Extrarebates(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()

class FatWallet(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()

class GivingAssistant(scrapy.Item):
	link 		= scrapy.Field()
	name 		= scrapy.Field()
	cashback 	= scrapy.Field()

class GoCashBack(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()

class HooplaDoopla(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()

class Iconsumer(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()

class LuckyShops(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()


class MainStreetShares(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()


class MrRebates(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field


class RebateBlast(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()

class RewardsAccelerator(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()

class ShopAtHome(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()

class SimplyBestCoupons(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()


class Splender(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()

class SunshineRewards(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()

class Yaging(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()
	sid 		= scrapy.Field()
	ctype 		= scrapy.Field()

class MileagePlanShopping(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()	

class AmtrakGuestRewards(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()	

class ChoicePrivilegeSmall(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	cashback 	= scrapy.Field()


class HawaiiAnairLines(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	miles 		= scrapy.Field()


class Hhonors(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	miles 		= scrapy.Field()

class Jetblue(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	points 		= scrapy.Field()

class Rewards(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	points 		= scrapy.Field()

class Southwest(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	points 		= scrapy.Field()

class Spirit(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	miles 		= scrapy.Field()

class FlyStore(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	points 		= scrapy.Field()

class BarclayCardRewardsboost(scrapy.Item):
	link 		= scrapy.Field()
	name		= scrapy.Field()
	points 		= scrapy.Field()

class Banks(scrapy.Item):
	Amex_Plenti_Marketplace		= scrapy.Field()
	BarclayCard_Rewardsboost	= scrapy.Field()
	Chase_UR_Freedom			= scrapy.Field()
	Chase_UR_Lnk				= scrapy.Field()
	Chase_UR_Sapphire			= scrapy.Field()
	Wells_Fargo_Rewards			= scrapy.Field()

	link 		= scrapy.Field()
	name		= scrapy.Field()
	points 		= scrapy.Field()
	best 		= scrapy.Field()
	bank 		= scrapy.Field()