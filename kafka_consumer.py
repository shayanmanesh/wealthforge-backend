"""
Kafka Consumer Service for WealthForge

Async message processing for analytics, notifications, and background tasks.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List
from kafka import KafkaConsumer
import redis
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WealthForgeKafkaConsumer:
    """Kafka consumer for processing WealthForge events."""
    
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = None
        self.consumers = {}
        self.running = False
        
        # Initialize Redis connection
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            self.redis_client.ping()
            logger.info("✅ Redis connection established for Kafka consumer")
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}")
            self.redis_client = None
    
    def start_consumers(self):
        """Start all Kafka consumers in separate threads."""
        self.running = True
        
        # Define topics and their handlers
        topics_handlers = {
            'goal_parsing_events': self.handle_goal_parsing_events,
            'strategy_optimization_events': self.handle_strategy_optimization_events,
            'portfolio_synthesis_events': self.handle_portfolio_synthesis_events,
            'compliance_audit_events': self.handle_compliance_audit_events,
            'fine_tuning_events': self.handle_fine_tuning_events,
            'market_data_requests': self.handle_market_data_requests,
            'economic_data_requests': self.handle_economic_data_requests,
            'complete_analysis_events': self.handle_complete_analysis_events
        }
        
        # Start consumer thread for each topic
        for topic, handler in topics_handlers.items():
            thread = threading.Thread(
                target=self._run_consumer,
                args=(topic, handler),
                daemon=True
            )
            thread.start()
            logger.info(f"🚀 Started consumer for topic: {topic}")
    
    def _run_consumer(self, topic: str, handler):
        """Run consumer for a specific topic."""
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=[self.bootstrap_servers],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id=f'wealthforge_{topic}_group',
                auto_offset_reset='latest',
                enable_auto_commit=True,
                consumer_timeout_ms=1000
            )
            
            self.consumers[topic] = consumer
            logger.info(f"📡 Consumer connected to topic: {topic}")
            
            while self.running:
                try:
                    for message in consumer:
                        if not self.running:
                            break
                        
                        try:
                            # Process message with handler
                            handler(message.value)
                            
                            # Store message processing metrics
                            self._store_processing_metrics(topic, message.value)
                            
                        except Exception as e:
                            logger.error(f"❌ Error processing message in {topic}: {e}")
                            self._store_error_metrics(topic, str(e))
                
                except Exception as e:
                    if "No more messages" not in str(e):
                        logger.error(f"❌ Consumer error for {topic}: {e}")
                    await asyncio.sleep(1)
        
        except Exception as e:
            logger.error(f"❌ Failed to start consumer for {topic}: {e}")
    
    def stop_consumers(self):
        """Stop all Kafka consumers."""
        self.running = False
        
        for topic, consumer in self.consumers.items():
            try:
                consumer.close()
                logger.info(f"🛑 Stopped consumer for topic: {topic}")
            except Exception as e:
                logger.error(f"❌ Error stopping consumer for {topic}: {e}")
        
        if self.redis_client:
            self.redis_client.close()
            logger.info("✅ Redis connection closed")
    
    # Event Handlers
    
    def handle_goal_parsing_events(self, message: Dict[str, Any]):
        """Handle goal parsing events."""
        logger.info(f"📋 Processing goal parsing event: {message.get('event_type')}")
        
        # Analytics tracking
        self._track_user_activity(
            message.get('user_id'),
            'goal_parsing',
            {
                'event_type': message.get('event_type'),
                'profile_complexity': message.get('profile_complexity'),
                'timestamp': message.get('timestamp')
            }
        )
        
        # Store parsing metrics
        if self.redis_client:
            try:
                key = f"metrics:goal_parsing:{datetime.now().strftime('%Y-%m-%d')}"
                self.redis_client.hincrby(key, 'total_parses', 1)
                self.redis_client.expire(key, 86400 * 7)  # Keep for 7 days
            except Exception as e:
                logger.error(f"❌ Redis metrics update failed: {e}")
    
    def handle_strategy_optimization_events(self, message: Dict[str, Any]):
        """Handle strategy optimization events."""
        logger.info(f"🏁 Processing strategy optimization event: {message.get('event_type')}")
        
        # Track strategy performance
        self._track_strategy_performance(message)
        
        # Trigger follow-up actions if needed
        if message.get('event_type') == 'strategy_optimized':
            self._trigger_portfolio_synthesis_notification(message)
    
    def handle_portfolio_synthesis_events(self, message: Dict[str, Any]):
        """Handle portfolio synthesis events."""
        logger.info(f"🔬 Processing portfolio synthesis event: {message.get('event_type')}")
        
        # Store portfolio performance metrics
        self._store_portfolio_metrics(message)
        
        # Trigger compliance audit notification
        if message.get('event_type') == 'portfolio_synthesized':
            self._trigger_compliance_audit_notification(message)
    
    def handle_compliance_audit_events(self, message: Dict[str, Any]):
        """Handle compliance audit events."""
        logger.info(f"⚖️ Processing compliance audit event: {message.get('event_type')}")
        
        # Track compliance metrics
        self._track_compliance_metrics(message)
        
        # Alert on violations
        if message.get('violations_count', 0) > 0:
            self._send_compliance_alert(message)
    
    def handle_fine_tuning_events(self, message: Dict[str, Any]):
        """Handle fine-tuning optimization events."""
        logger.info(f"🔧 Processing fine-tuning event: {message.get('event_type')}")
        
        # Track optimization performance
        self._track_optimization_metrics(message)
        
        # Notify on significant improvements
        improvement_factor = message.get('improvement_factor', 1.0)
        if improvement_factor > 2.0:  # 100%+ improvement
            self._send_optimization_success_notification(message)
    
    def handle_market_data_requests(self, message: Dict[str, Any]):
        """Handle market data request events."""
        logger.info(f"📊 Processing market data request: {message.get('event_type')}")
        
        # Track data usage
        self._track_data_usage('market_data', message)
    
    def handle_economic_data_requests(self, message: Dict[str, Any]):
        """Handle economic data request events."""
        logger.info(f"📈 Processing economic data request: {message.get('event_type')}")
        
        # Track data usage
        self._track_data_usage('economic_data', message)
    
    def handle_complete_analysis_events(self, message: Dict[str, Any]):
        """Handle complete analysis events."""
        logger.info(f"🌟 Processing complete analysis event: {message.get('event_type')}")
        
        # Track complete analysis metrics
        self._track_complete_analysis_metrics(message)
        
        # Send completion notification
        self._send_analysis_completion_notification(message)
    
    # Helper Methods
    
    def _track_user_activity(self, user_id: str, activity_type: str, data: Dict[str, Any]):
        """Track user activity for analytics."""
        if not self.redis_client or not user_id:
            return
        
        try:
            # Store user activity
            activity_key = f"user_activity:{user_id}:{activity_type}"
            activity_data = {
                'timestamp': datetime.now().isoformat(),
                'activity_type': activity_type,
                **data
            }
            
            self.redis_client.lpush(activity_key, json.dumps(activity_data))
            self.redis_client.ltrim(activity_key, 0, 99)  # Keep last 100 activities
            self.redis_client.expire(activity_key, 86400 * 30)  # Keep for 30 days
            
            # Update activity counters
            counter_key = f"counters:user:{user_id}:{activity_type}"
            self.redis_client.incr(counter_key)
            self.redis_client.expire(counter_key, 86400 * 30)
            
        except Exception as e:
            logger.error(f"❌ User activity tracking failed: {e}")
    
    def _track_strategy_performance(self, message: Dict[str, Any]):
        """Track strategy optimization performance."""
        if not self.redis_client:
            return
        
        try:
            # Store strategy metrics
            date_key = datetime.now().strftime('%Y-%m-%d')
            metrics_key = f"metrics:strategy:{date_key}"
            
            self.redis_client.hincrby(metrics_key, 'total_optimizations', 1)
            
            if 'num_agents' in message:
                self.redis_client.hset(metrics_key, 'avg_agents', message['num_agents'])
            
            if 'execution_time' in message:
                # Store execution time statistics
                exec_time = message['execution_time']
                self.redis_client.lpush(f"performance:strategy_exec_times", exec_time)
                self.redis_client.ltrim(f"performance:strategy_exec_times", 0, 999)
            
            self.redis_client.expire(metrics_key, 86400 * 7)
            
        except Exception as e:
            logger.error(f"❌ Strategy performance tracking failed: {e}")
    
    def _store_portfolio_metrics(self, message: Dict[str, Any]):
        """Store portfolio synthesis metrics."""
        if not self.redis_client:
            return
        
        try:
            date_key = datetime.now().strftime('%Y-%m-%d')
            metrics_key = f"metrics:portfolio:{date_key}"
            
            self.redis_client.hincrby(metrics_key, 'total_syntheses', 1)
            
            # Store performance metrics
            if 'expected_return' in message:
                returns_key = f"performance:portfolio_returns"
                self.redis_client.lpush(returns_key, message['expected_return'])
                self.redis_client.ltrim(returns_key, 0, 999)
            
            if 'risk_score' in message:
                risk_key = f"performance:portfolio_risks"
                self.redis_client.lpush(risk_key, message['risk_score'])
                self.redis_client.ltrim(risk_key, 0, 999)
            
            self.redis_client.expire(metrics_key, 86400 * 7)
            
        except Exception as e:
            logger.error(f"❌ Portfolio metrics storage failed: {e}")
    
    def _track_compliance_metrics(self, message: Dict[str, Any]):
        """Track compliance audit metrics."""
        if not self.redis_client:
            return
        
        try:
            date_key = datetime.now().strftime('%Y-%m-%d')
            metrics_key = f"metrics:compliance:{date_key}"
            
            self.redis_client.hincrby(metrics_key, 'total_audits', 1)
            
            # Track compliance scores
            if 'audit_score' in message:
                scores_key = f"performance:compliance_scores"
                self.redis_client.lpush(scores_key, message['audit_score'])
                self.redis_client.ltrim(scores_key, 0, 999)
            
            # Track violations
            violations_count = message.get('violations_count', 0)
            if violations_count > 0:
                self.redis_client.hincrby(metrics_key, 'total_violations', violations_count)
            
            self.redis_client.expire(metrics_key, 86400 * 7)
            
        except Exception as e:
            logger.error(f"❌ Compliance metrics tracking failed: {e}")
    
    def _track_optimization_metrics(self, message: Dict[str, Any]):
        """Track fine-tuning optimization metrics."""
        if not self.redis_client:
            return
        
        try:
            date_key = datetime.now().strftime('%Y-%m-%d')
            metrics_key = f"metrics:optimization:{date_key}"
            
            self.redis_client.hincrby(metrics_key, 'total_optimizations', 1)
            
            # Track improvement factors
            if 'improvement_factor' in message:
                improvements_key = f"performance:improvement_factors"
                self.redis_client.lpush(improvements_key, message['improvement_factor'])
                self.redis_client.ltrim(improvements_key, 0, 999)
            
            self.redis_client.expire(metrics_key, 86400 * 7)
            
        except Exception as e:
            logger.error(f"❌ Optimization metrics tracking failed: {e}")
    
    def _track_data_usage(self, data_type: str, message: Dict[str, Any]):
        """Track external data API usage."""
        if not self.redis_client:
            return
        
        try:
            date_key = datetime.now().strftime('%Y-%m-%d')
            usage_key = f"usage:{data_type}:{date_key}"
            
            self.redis_client.hincrby(usage_key, 'requests', 1)
            
            # Track symbols for market data
            if data_type == 'market_data' and 'symbols' in message:
                for symbol in message['symbols']:
                    self.redis_client.hincrby(usage_key, f'symbol_{symbol}', 1)
            
            # Track series for economic data
            if data_type == 'economic_data' and 'series_id' in message:
                self.redis_client.hincrby(usage_key, f'series_{message["series_id"]}', 1)
            
            self.redis_client.expire(usage_key, 86400 * 30)  # Keep for 30 days
            
        except Exception as e:
            logger.error(f"❌ Data usage tracking failed: {e}")
    
    def _track_complete_analysis_metrics(self, message: Dict[str, Any]):
        """Track complete analysis metrics."""
        if not self.redis_client:
            return
        
        try:
            date_key = datetime.now().strftime('%Y-%m-%d')
            metrics_key = f"metrics:complete_analysis:{date_key}"
            
            self.redis_client.hincrby(metrics_key, 'total_analyses', 1)
            
            # Track execution time
            if 'execution_time' in message:
                exec_times_key = f"performance:complete_analysis_times"
                self.redis_client.lpush(exec_times_key, message['execution_time'])
                self.redis_client.ltrim(exec_times_key, 0, 999)
            
            self.redis_client.expire(metrics_key, 86400 * 7)
            
        except Exception as e:
            logger.error(f"❌ Complete analysis metrics tracking failed: {e}")
    
    def _store_processing_metrics(self, topic: str, message: Dict[str, Any]):
        """Store general message processing metrics."""
        if not self.redis_client:
            return
        
        try:
            # Update message processing counters
            date_key = datetime.now().strftime('%Y-%m-%d')
            processing_key = f"processing:{topic}:{date_key}"
            
            self.redis_client.hincrby(processing_key, 'messages_processed', 1)
            self.redis_client.hset(processing_key, 'last_processed', datetime.now().isoformat())
            self.redis_client.expire(processing_key, 86400 * 7)
            
        except Exception as e:
            logger.error(f"❌ Processing metrics storage failed: {e}")
    
    def _store_error_metrics(self, topic: str, error_message: str):
        """Store error metrics for monitoring."""
        if not self.redis_client:
            return
        
        try:
            date_key = datetime.now().strftime('%Y-%m-%d')
            error_key = f"errors:{topic}:{date_key}"
            
            self.redis_client.hincrby(error_key, 'error_count', 1)
            self.redis_client.hset(error_key, 'last_error', error_message)
            self.redis_client.hset(error_key, 'last_error_time', datetime.now().isoformat())
            self.redis_client.expire(error_key, 86400 * 7)
            
        except Exception as e:
            logger.error(f"❌ Error metrics storage failed: {e}")
    
    # Notification Methods (placeholders for future implementation)
    
    def _trigger_portfolio_synthesis_notification(self, message: Dict[str, Any]):
        """Trigger notification to start portfolio synthesis."""
        logger.info(f"📧 Portfolio synthesis notification triggered for user {message.get('user_id')}")
    
    def _trigger_compliance_audit_notification(self, message: Dict[str, Any]):
        """Trigger notification to start compliance audit."""
        logger.info(f"📧 Compliance audit notification triggered for portfolio {message.get('portfolio_id')}")
    
    def _send_compliance_alert(self, message: Dict[str, Any]):
        """Send alert for compliance violations."""
        violations_count = message.get('violations_count', 0)
        logger.warning(f"🚨 Compliance alert: {violations_count} violations detected for user {message.get('user_id')}")
    
    def _send_optimization_success_notification(self, message: Dict[str, Any]):
        """Send notification for successful optimization."""
        improvement = message.get('improvement_factor', 1.0)
        logger.info(f"🎉 Optimization success notification: {improvement:.1f}x improvement for user {message.get('user_id')}")
    
    def _send_analysis_completion_notification(self, message: Dict[str, Any]):
        """Send notification for completed analysis."""
        logger.info(f"✅ Analysis completion notification sent to user {message.get('user_id')}")

def main():
    """Main function to run Kafka consumers."""
    logger.info("🚀 Starting WealthForge Kafka Consumer Service")
    
    consumer_service = WealthForgeKafkaConsumer()
    
    try:
        consumer_service.start_consumers()
        logger.info("📡 All Kafka consumers started successfully")
        
        # Keep the service running
        while True:
            asyncio.sleep(10)
    
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down Kafka consumers...")
        consumer_service.stop_consumers()
        logger.info("👋 Kafka consumer service stopped")
    
    except Exception as e:
        logger.error(f"❌ Kafka consumer service failed: {e}")
        consumer_service.stop_consumers()

if __name__ == "__main__":
    main()